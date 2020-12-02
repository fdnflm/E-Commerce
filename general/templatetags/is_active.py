from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag
def is_active(request, url):
	# проверка если текущий url совпадает с данным в аргументе
	if len(request.path) > 1 and request.path in reverse(url) or request.path == reverse(url):
		return "active"
	return ""
