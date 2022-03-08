from django import forms
from django.forms import ModelForm
from product.models import Product
from allauth.account.forms import SignupForm, LoginForm

from .models import User

class AddProduct(ModelForm):
    """Lets Shopowner add products"""
    
    class Meta:
         model = Product
         fields = "__all__"
    