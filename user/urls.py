from django.urls import path
from .views import OrdersView, view_order, user_profile, add_premium, download_order

app_name = 'user'

urlpatterns = [
	path('orders/', OrdersView.as_view(), name='orders'),
	path('order/<transaction_id>', view_order, name='view_order'),
	path('settings/', user_profile, name='settings'),
	path('get_premium/', add_premium, name='add_premium'),
	path('download_order/<transaction_id>', download_order, name='download_order')
]