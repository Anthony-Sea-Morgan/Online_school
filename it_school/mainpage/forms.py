from django import forms
from .models import CustomUser


class ProfileForm(forms.ModelForm):
    """
    Форма профиля пользователя.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class WalletForm(forms.ModelForm):
    """
    Форма кошелька пользователя.
    """
    class Meta:
        model = CustomUser
        fields = ['wallet']
    widgets ={
        'wallet': forms.NumberInput(attrs={'class': 'form-group', 'type': 'number'}),
    }