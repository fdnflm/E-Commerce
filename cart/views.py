from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages
from general.models import Product, Order, OrderItem
from .models import Cart


def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # если товар закончился
    if product.amount == 0:
        messages.error(request, 'Товар невозможно добавить в корзину')
        return redirect('general:item', product.id)
    if cart.add(product):
        messages.info(request, 'Добавлено в корзину')
    else:
        # если в корзине макс. кол-во товара
        messages.error(request, 'Добавлено максимальное кол-во товара')
    return redirect('cart:index')


def remove(request, product_id, full):  # удаление товара
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # если аргумент full == 'full', то товар полностью удаляется из корзины
    # иначе, кол-во уменьшается на 1 единицу
    cart.remove(product, full)
    messages.info(request, 'Удалено из корзины')
    return redirect('cart:index')


def clear(request):  # очищаем корзину от товаров
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Корзина очищена')
    return redirect('cart:index')


def index(request):  # сама корзина
    return render(request, 'cart/index.html')


@login_required
def complete_order(request):
    cart = Cart(request)
    # если в корзине ничего нет, заказ оформить не получится
    if cart.is_empty():
        return redirect('cart:index')
    return render(request, 'cart/make_order.html', {'price': cart.get_total_price()})


@login_required
def payment_hook(request):
    cart = Cart(request)
    # если в корзине ничего нет, заказ оформить не получится
    if cart.is_empty():
        return redirect('cart:index')
    # получаем заказ, который не был оформлен
    order = Order.objects.get(customer=request.user, complete=False)
    # заказ готов
    order.complete = True
    order.status = 'Ожидает получения'
    order.set_transaction_id()
    order.save()
    # отнимаем кол-во продукта из бд
    for item in order.items.all():
        product = Product.objects.get(pk=item.product.id)
        product.amount -= item.amount
        product.save()
    return redirect('user:orders')
