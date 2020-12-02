from django import forms
from general.models import User


class ChangeInfoForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Имя пользователя'
               }
    ), label='Никнейм', max_length=32)

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Имя'
               }
    ), label="Имя", max_length=32)

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Фамилия'
               }
    ), label="Фамилия", max_length=32)

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'placeholder': 'Почта'
               }
    ), label="Почта", max_length=100)

    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Телефон'
               }
    ), label="Номер телефона", min_length=11, max_length=11, required=False)

    telegram = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Telegram'
               }
    ), label="Telegram", max_length=32, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'telegram')
