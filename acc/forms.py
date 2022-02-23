"""module defines all the form used all ove the project"""
from django import forms

from allauth.account.forms import SignupForm, LoginForm

from .models import Product, User


class AdminUserUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    full_name = forms.CharField(max_length=50)



class CustomerSignupForm(SignupForm):
    """form for customer to sign up"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    genderchoices = [
        ("M", "Male"),
        ("F", "Female")
    ]

    full_name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(
        label='date_of_birth', widget=forms.SelectDateWidget,)
    gender = forms.ChoiceField(choices=genderchoices)

    class Meta:
        """meta attributes for this class"""
        model = User

    def save(self, request):
        user = User()
        user.role = "customer"
        user.email = self.cleaned_data['email']
        user.set_password(user.password)
        user.full_name = self.cleaned_data['full_name']
        user.address = self.cleaned_data['address']
        user.gender = self.cleaned_data['gender']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user


class ShopSignupForm(SignupForm):
    """form for shop to sign up"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    genderchoices = [
        ("M", "Male"),
        ("F", "Female")
    ]
    full_name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(
        label='date_of_birth', widget=forms.SelectDateWidget,)
    gender = forms.ChoiceField(choices=genderchoices)
    shopname = forms.CharField(max_length=50)
    shopaddress = forms.CharField(max_length=200)
    shopdesc = forms.CharField(max_length=500)
    role = "shopowner"

    class Meta:
        """meta attribute for this class"""
        model = User


class AddUserForm(SignupForm):
    """form for shop to sign up"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    genderchoices = [
        ("M", "Male"),
        ("F", "Female")
    ]
    full_name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(
        label='date_of_birth', widget=forms.SelectDateWidget,)
    gender = forms.ChoiceField(choices=genderchoices)
    shopname = forms.CharField(max_length=50)
    shopaddress = forms.CharField(max_length=200)
    shopdesc = forms.CharField(max_length=500)
    role = forms.CharField(max_length=50)

    class Meta:
        """meta attribute for this class"""
        model = User


class UserLoginForm(LoginForm):
    """form for user login"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        """meta attribtes"""
        model = User


class RequestResponseForm(forms.Form):
    """Form for aadmin to approve or reject a shop registration"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    choices = [
        ("approve", "approve"),
        ("reject", "reject")
    ]

    class Meta:
        """meta attribute for this class"""
        model = User
        fields = []

    response = forms.ChoiceField(choices=choices)

class AddShop(forms.Form):
    categories = (("electronics","electronics") , ("footwear","footwear") , ("accesories","accesories"))
    name = forms.CharField()
    price = forms.IntegerField()
    category = forms.ChoiceField(choices=categories)
    description = forms.CharField()
    image = forms.ImageField()
    brand = forms.CharField()
    quantity = forms.IntegerField()
    