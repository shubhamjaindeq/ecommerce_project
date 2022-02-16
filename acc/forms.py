
from django import forms

from allauth.account.forms import SignupForm, LoginForm
from django.db.models.signals import post_save
from .models import MyUser


class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': "form-control input-lg"})
        self.fields['password1'].widget = forms.TextInput(attrs={'class': "form-control input-lg" , 'placeholder': "sldhk" })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control input-lg'})
        #print(self)
    genderchoices = [
        ("M", "Male"),
        ("F", "Female")
    ]
    roles = [("admin", "admin") , ("shopowner", "shopowner") ,("customer","customer")]
    full_name = forms.CharField(max_length=30, label='full_name', widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': 'full_name'
        }))
    address = forms.CharField(max_length=30, label='address',widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': 'full_name'
        }))

    role = forms.ChoiceField(choices=roles)
    date_of_birth = forms.DateField(
        label='date_of_birth', widget=forms.SelectDateWidget,)
    gender = forms.ChoiceField(choices=genderchoices )
    

    class Meta:
        model = MyUser

    def save(self, request):
        # post_save.disconnect(MyUser)
        #user = super().save(request )
        # post_save.connect(MyUser)
        user = MyUser()
        a = self.cleaned_data['role']
        if a == "shopowner":
            user.is_active = False
        user.email = self.cleaned_data['email'] 
        user.password = self.cleaned_data['password2']
        print("password is",user.password)
        user.role = self.cleaned_data['role']
        print(user.role , "is after first save is called")
        user.full_name = self.cleaned_data['full_name']
        user.address = self.cleaned_data['address']
        user.gender = self.cleaned_data['gender']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user


class MyLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class': "form-control input-lg"})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control input-lg'})
    class Meta: 
        model = MyUser

class EditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': "form-control input-lg"})
        self.fields['full_name'].widget = forms.TextInput(attrs={'class': "form-control input-lg"})
        self.fields['address'].widget = forms.TextInput(attrs={'class': "form-control input-lg"})
        
    class Meta:
            model = MyUser
            fields = [
            "email",
            "full_name",
            "address",
            ]
            
    