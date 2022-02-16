from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.shortcuts import get_object_or_404,HttpResponseRedirect


class MyUserManager(BaseUserManager):

    def create_user(self, full_name=None, date_of_birth=None, email=None, gender=None,
                    address=None, is_shop_user=False,role = "customer", password=None):

        if not email:
            raise ValueError('Users must have an email address attached ')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            role = role
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
        user.role = "admin"
        user.save()
        return user


class MyUser(AbstractBaseUser):
    roles = [('admin','admin') , ('shopowner','shopowner') ,('customer','customer')]
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
    role = models.CharField(max_length=10 , choices=roles, default="customer")
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

class Shop(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

