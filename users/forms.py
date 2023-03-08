from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите Ваш будущий логин'
    }))
    email = forms.CharField(widget=forms.EmailInput())
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')