from django.urls import path, include
from .views import user_login, user_register

urlpatterns = [
    path('login/', user_login,name='login'),
    path('register/', user_register, name='register'),
    path('', include('django.contrib.auth.urls'))
]
