from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.shortcuts import get_object_or_404,HttpResponseRedirect

from acc.forms import EditForm

class MyUserManager(BaseUserManager):
    def create_user(self, full_name=None, date_of_birth=None, email=None, gender=None,
                    address=None, is_shop_user=False, password=None):

        if not email:
            raise ValueError('Users must have an email address attached ')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            is_shop_user=is_shop_user
        )
        user.is_active = True
        user.is_staff = False
        user.is_admin = False
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,  full_name=None, date_of_birth=None,is_shop_user = False ,  email=None, gender=None,
                         address=None, password=None):

        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
            gender=gender,
            address=address,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.is_staff = True
        user.is_shop_user = False
        user.save()
        return user


class MyUser(AbstractBaseUser):
    genderchoices = [
        ("M", "Male"),
        ("F", "Female")
    ]
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    full_name = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=genderchoices, null=True)
    address = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_shop_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_sstaff(self):

        return self.is_admin

    def is_shopU(self):

        return self.is_shop_user

def update_view(request, id):
   
    context ={}
    obj = get_object_or_404(Myuser, id = id)
 
    
    form = EditForm(request.POST or None, instance = obj)
 
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+id)