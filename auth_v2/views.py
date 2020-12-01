from django.shortcuts import render, redirect, reverse
from .forms import UserLoginForm, UserRegForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from cart.models import Cart


def user_login(request):
    if request.user.is_authenticated:  # если пользователь авторизован редиректим на главную
        return redirect(reverse('general:index'))

    if request.method == 'POST':  # если запрос на вход
        next_page = request.POST.get('next')  # для редиректа после авторизации
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])  # пробуем войти
            if user is not None:
                if user.is_active:  # успешный вход
                    login(request, user)
                    cart = Cart(request, first_login=True)
                    if cd['merge']:  # синхронизируем корзину с БД
                        cart.set_order_from_session()
                    messages.info(request, "Авторизация прошла успешно")
                    redirect_url = settings.LOGIN_REDIRECT_URL if not next_page else next_page
                    return redirect(redirect_url)
                else:  # вход не очень успешный :(
                    return HttpResponse('Disabled account')
    else:
        form = UserLoginForm(request)

    context = {'form': form, 'next': request.GET['next']}
    return render(request, 'auth_v2/login.html', context)


def user_register(request):
    if request.user.is_authenticated:
        return redirect(reverse('general:index'))

    if request.method == 'POST':
        form = UserRegForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Регистрация прошла успешно")
            return redirect(reverse('login'))
    else:
        form = UserRegForm()

    context = {'form': form}
    return render(request, 'auth_v2/register.html', context)


def logout_user(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
