from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .models import Product, Promo, Order, OrderItem
from django.http import HttpResponse


def index(request):
    # получаем товары
    # получаем баннеры
    context = {
        'products': Product.objects.order_by('-date_created'),
        'promos': Promo.objects.all(),
        'top_day': []
    }
    # проверяем есть ли баннеры для карусели и добавляем их в список
    for promo in context['promos']:
        if promo.promo_type == 'top_day' and promo.enabled and promo.is_future_due:
            context['top_day'].append(promo)

    return render(request, "general/index.html", context)


class ItemView(generic.DetailView):
    template_name = "general/item.html"
    model = Product
    context_object_name = "product"
