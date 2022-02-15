
from django import forms

from allauth.account.forms import SignupForm, LoginForm

from . models import MyUser


class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': "form-control input-lg"})
        self.fields['password1'].widget = forms.TextInput(attrs={'class': "form-control input-lg" , 'placeholder': "sldhk" })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control input-lg'})
        print(self)
    genderchoices = [
        ("M", "Male"),
        ("F", "Female")
    ]
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
    date_of_birth = forms.DateField(
        label='date_of_birth', widget=forms.SelectDateWidget,)
    gender = forms.ChoiceField(choices=genderchoices )

    class Meta:
        model = MyUser

    def save(self, request):

        user = super().save(request)
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

class EditForm(forms.Form):
    def __init__(self,*args,**kwargs):
        email = forms.EmailField(label = "email" , widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'email'
        }) )