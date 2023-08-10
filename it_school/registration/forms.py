from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1')


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={'class': 'blank-input'}))
    last_name = forms.CharField(label='Фамилия:', widget=forms.TextInput(attrs={'class': 'blank-input'}))
    email = forms.EmailField(label='Почтовый адрес:', widget=forms.TextInput(attrs={'class': 'blank-input'}))
    phone_number = PhoneNumberField(label='Номер телефона:', widget=forms.TextInput(attrs={'class': 'blank-input'}))
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'blank-input'}))
    password2 = forms.CharField(label='Подтверждение пароля:', widget=forms.PasswordInput(attrs={'class': 'blank-input'}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email', 'phone_number', 'password1', 'password2')