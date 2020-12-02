from .models import Cart


def cart(request):
	return {'cart': Cart(request)}


def tasty_price(request, price):
	return price / 100 * 90
