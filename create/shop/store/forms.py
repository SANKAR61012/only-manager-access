from django import forms
from .models import Product, CustomUser
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']
