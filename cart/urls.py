from django.urls import path

from .views import index, add, remove, clear, complete_order, payment_hook

app_name = 'cart'

urlpatterns = [
    path('', index, name='index'),
    path('add/<int:product_id>/', add, name='cart_add'),
    path('remove/<int:product_id>/<str:full>', remove, name='cart_remove'),
    path('clear/', clear, name='cart_clear'),
    path('checkout/', complete_order, name='make_order'),
    path('payment/', payment_hook, name='payment_hook'),
]
