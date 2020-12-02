from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from general.models import Order, User
from django.http import FileResponse, HttpResponseForbidden
from user.forms import ChangeInfoForm
import zipfile
import random
import os


@login_required
def user_profile(request):
	initial_data = {
		'username': request.user.username,
		'first_name': request.user.first_name,
		'last_name': request.user.last_name,
		'email': request.user.email,
		'phone_number': request.user.phone_number,
		'telegram': request.user.telegram
	}
	if request.POST:
		change_info_form = ChangeInfoForm(request.POST, initial=initial_data, instance=request.user)
		if change_info_form.is_valid():
			change_info_form.save()
	else:
		change_info_form = ChangeInfoForm(initial=initial_data)
	return render(request, 'user/settings.html', {'form': change_info_form})


@login_required
def add_premium(request):
	if request.method == "POST":
		days = 0
		if request.POST.get('days') == '1':
			days = 30
		elif request.POST.get('days') == '2':
			days = 90
		elif request.POST.get('days') == '3':
			days = 365
		request.user.set_paid(days=days)
	return redirect(reverse('user:settings'))


class OrdersView(generic.ListView):
	template_name = 'user/orders.html'
	context_object_name = 'orders'

	def get_queryset(self):
		return Order.objects.filter(complete=True, customer=self.request.user).all()


@login_required
def view_order(request, transaction_id):
	order = get_object_or_404(Order, transaction_id=transaction_id)
	context = {'order': order}
	return render(request, 'user/order.html', context)


@login_required
def download_order(request, transaction_id):
	order = get_object_or_404(Order, transaction_id=transaction_id)
	if order.customer != request.user:
		return HttpResponseForbidden()
	order_items = order.items.all()
	path_to_zip = f'media/orders/order_{order.transaction_id}.zip'
	if not os.path.exists(path_to_zip):
		with zipfile.ZipFile(path_to_zip, 'w') as order_zip:
			for item in order_items:
				for piece in range(item.amount):
					selected_item = random.choice(os.listdir(f"media/files/{item.product.slug}"))
					order_zip.write(f'media/files/{item.product.slug}/{selected_item}', )
					os.remove(f"media/files/{item.product.slug}/{selected_item}")

			order_zip.close()
		order.status = "Получено"
		order.save()
	return FileResponse(open(path_to_zip, 'rb'))

