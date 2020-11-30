from .forms import UserRegForm
from django.urls import reverse_lazy, resolve
from django.shortcuts import redirect
from django.views import generic
from .settings import LOGIN_REDIRECT_URL

class SignUpView(generic.CreateView):
	form_class = UserRegForm
	success_url = reverse_lazy('login')
	template_name = 'registration/register.html'


def anonymous_required(func):
    def as_view(request, **kwargs):
        redirect_to = kwargs.get('next', LOGIN_REDIRECT_URL )
        if request.user.is_authenticated:
            return redirect(redirect_to)
        response = func(request, **kwargs)
        return response
    return as_view
