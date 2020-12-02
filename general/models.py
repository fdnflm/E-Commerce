from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import random
from django.conf import settings
import string
import random
from django.utils.text import slugify
import datetime
from django.core.validators import MinLengthValidator


class BaseModel(models.Model):
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True, unique=True,
                                    validators=[MinLengthValidator(11)])
    telegram = models.CharField(max_length=32, null=True, blank=True, unique=True, validators=[MinLengthValidator(5)])
    avatar = models.ImageField(default=f"default_avatars/{random.randint(1, 50)}.png", upload_to='avatars/')
    paid_until = models.DateTimeField(verbose_name="Подписка до", null=True, blank=True)  # подписка
    discount = models.IntegerField(default=0, blank=True)  # персональная скидка пользователя
    bonus = models.IntegerField(default=0, blank=True)  # бонусы

    def is_premium(self):  # проверяем, имеет ли пользователь подписку
        if not self.paid_until:
            return False
        is_premium = self.paid_until > timezone.now()
        if self.discount > 0 and not is_premium:  # убираем скидку если подписка закончилась
            self.discount = 0
            self.save()
        return is_premium

    def set_paid(self, days, discount=10):
        self.discount = discount
        start_date = self.paid_until if self.paid_until > timezone.now() else timezone.now()
        self.paid_until = start_date + datetime.timedelta(days)
        self.save()


class Product(BaseModel, models.Model):
    name = models.CharField(max_length=32, verbose_name='Имя продукта')
    description = models.TextField(verbose_name='Описание', max_length=250, null=True)
    items_catalog = models.FileField(upload_to=f'files/', null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    price = models.FloatField(verbose_name='Цена, руб')
    amount = models.IntegerField(default=1, verbose_name='Кол-во')
    discount = models.IntegerField(default=0, verbose_name='Скидка %')
    slug = models.SlugField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(BaseModel, models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=32, default='В обработке',
                              choices=(('В обработке', 'В обработке'),
                                       ('Ожидает получения', 'Ожидает получения'),
                                       ('Получено', 'Получено'),
                                       ('Возврат', 'Возврат'),
                                       ('Отменено', 'Отменено')))
    transaction_id = models.CharField(default="",
                                      max_length=200,
                                      null=True,
                                      blank=True)

    class Meta:
        ordering = ("-date_created",)

    def set_transaction_id(self):
        self.transaction_id = "".join(random.choice(string.ascii_lowercase) for i in range(16))

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Заказ #{self.id}"


class OrderItem(BaseModel, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(default=1)
    discounted_price = models.FloatField(default=0)

    class Meta:
        ordering = ("-date_created",)

    @property
    def total_price(self):
        return self.amount * self.discounted_price

    def __str__(self):
        return f"Элемент<{self.order.id}>"


class Promo(models.Model):
    image = models.ImageField(upload_to='images/')
    promo_type = models.CharField(max_length=32, choices=[('top_day', 'top_day'), ('side_ad', 'side_ad')])
    linked_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    @property
    def is_future_due(self):
        if not self.end_date and self.enabled:
            return True
        return self.end_date > timezone.now()

    def __str__(self):
        return f"Promo<{self.promo_type}>"
