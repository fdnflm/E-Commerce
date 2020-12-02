from django.contrib import admin
from .models import User, Product, Order, OrderItem, Promo
from django.utils.text import slugify
import os
import zipfile


class OrderItemInline(admin.StackedInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)  # product-name-some
        obj.save()
        if obj.items_catalog:  # сохранение товаров в .zip формате
            zip_file = zipfile.ZipFile(obj.items_catalog.path)
            prev_path = 0
            if os.path.exists(f'media/files/{obj.slug}'):
                prev_path = len(os.listdir(f'media/files/{obj.slug}'))
            obj.amount = prev_path + len(zip_file.namelist())
            zip_file.extractall(f'media/files/{obj.slug}')
            zip_file.close()
            os.remove(obj.items_catalog.path)
            obj.items_catalog = ''
            obj.save()


admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Promo)
