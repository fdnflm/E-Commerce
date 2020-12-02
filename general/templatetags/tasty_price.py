from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag
def tasty_price(product, user_discount):
    user_discount = user_discount if user_discount else 0  # pFix для анонимного юзера
    total_discount = product.discount + user_discount
    return "{0:.2f}".format(product.price / 100 * (100 - total_discount))
