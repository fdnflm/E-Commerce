from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Имя пользователя'
               }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }
    ))
    merge = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(
        attrs={
            'class': 'custom-control-input',
            'id': 'customCheck'
        }
    ))


class UserRegForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Имя пользователя'
               }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        }
    ))

    class Meta:
        model = get_user_model() # для кастом модели юзера
        fields = ('username', 'password1', 'password2')
