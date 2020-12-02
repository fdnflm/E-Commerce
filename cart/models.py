from django.db import models
from django.conf import settings
from general.models import Product, Order, OrderItem
from general.templatetags.tasty_price import tasty_price


class Cart(object):
    def __init__(self, request, first_login=False):  # инициализация экземпляра корзины
        self.logged_in = request.user.is_authenticated
        self.user = request.user
        self.user_discount = 0
        try:  # пытаемся получить скидку у пользователя если она есть для формирования цен
            self.user_discount = self.user.discount
        except Exception:
            self.user_discount = 0
        self.session = request.session
        if self.logged_in and not first_login:  # если юзер вошёл, загружаем коризну из БД
            self.cart = {}
            self.set_cart_from_db()
        else:
            self.cart = self.session.get(settings.CART_ID)  # если нет, то формируем корзину из сессии
            if not self.cart:
                self.cart = self.session[settings.CART_ID] = {}

    def add(self, product):
        if self.logged_in:  # добавляем товар в заказ в БД
            order = Order.objects.get(customer=self.user, complete=False)
            item, created = OrderItem.objects.get_or_create(order=order,
                                                            product=product,
                                                            discounted_price=float(
                                                                tasty_price(product, self.user_discount)))
            if item.amount == product.amount:  # кол-во товара ограничено
                return False
            if not created:  # если товар уже есть в заказе, увеличиваем кол-во
                item.amount += 1
                item.save()
        else:  # если юзер анонимен
            product_id = str(product.id)
            if product_id not in self.cart:  # создаем новый продукт в сессии
                self.cart[product_id] = {'amount': 0, 'price': float(tasty_price(product, self.user_discount))}
            else:  # если кол-во продукта в корзине достигает доступного в БД даём ошибку
                if self.cart[str(product.id)]['amount'] == product.amount:
                    return False

            self.cart[product_id]['amount'] += 1
            self.save()

        return True

    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def remove(self, product, full):
        product_id = str(product.id)
        if self.logged_in:
            order = Order.objects.get(customer=self.user, complete=False)
        if product_id in self.cart:  # если товар в корзине
            if full == "not_full":  # удаляем частично на одну единицу
                if self.cart[product_id]['amount'] > 1:
                    if self.logged_in:
                        item = OrderItem.objects.get(order_id=order.id, product=product)
                        item.amount -= 1
                        item.save()
                    else:
                        self.cart[product_id]['amount'] -= 1
                else:  # если кол-во товара = 1, то удаляем из корзины полностью
                    if self.logged_in:
                        item = OrderItem.objects.get(order_id=order.id, product=product)
                        item.delete()
                    else:
                        del self.cart[product_id]
            elif full == "full":  # полнаое удаление товара из корзины
                if self.logged_in:
                    item = OrderItem.objects.get(order_id=order.id, product=product)
                    item.delete()
                else:
                    del self.cart[product_id]
            self.save()

    def set_order_from_session(self):  # загрузка товарова из корзины в БД (слияние корзины)
        if self.logged_in:
            order, created = Order.objects.get_or_create(customer=self.user, complete=False)  # создаем новый заказ
            for cart_item in self.cart.items():  # добавляем каждый продукт в заказ БД
                db_items = order.items.all()
                counter = 0
                for db_item in db_items:  # проходимся по БД и добавляем новые товары
                    if db_item.product.id == int(cart_item[0]):
                        counter += 1
                        db_item.discounted_price = cart_item[1]['price']
                        db_item.amount += cart_item[1]['amount']
                        db_item.save()
                if counter == 0:  # если товара еще нет в БД, добавляем
                    order_item = OrderItem(order=order, product_id=cart_item[0], amount=cart_item[1]['amount'],
                                           discounted_price=cart_item[1]['price'])
                    order_item.save()
            return True
        return False  # нет входа в систему

    def set_cart_from_db(self):
        # загружаем товары в сессию из БД для контекстного процессора
        # для дальнейшего отображения в темплейтах
        order, created = Order.objects.get_or_create(customer=self.user, complete=False)
        for item in order.items.all():
            self.cart[str(item.product.id)] = {'amount': item.amount,
                                               'price': float(tasty_price(item.product, self.user_discount))}

    def get_total_price(self):
        # получаем полную стоимость товаров в корзине
        return sum(item['price'] * item['amount'] for item in self.cart.values())

    def clear(self):  # очищаем корзину полностью
        del self.session[settings.CART_ID]
        if self.logged_in:
            order = Order.objects.get(customer=self.user, complete=False)
            order.items.all().delete()
        self.session.modified = True

    def is_empty(self):
        return len(self.cart) == 0

    def __iter__(self):  # для циклов for
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = item['price'] * item['amount']
            yield item

    def __len__(self):
        return sum(item['amount'] for item in self.cart.values())

    def __str__(self):
        return f"Корзина: {self.cart}"

    def __repr__(self):
        return f"Корзина: {self.cart}"
