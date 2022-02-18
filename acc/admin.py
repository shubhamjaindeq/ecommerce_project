from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group

from acc.models import MyUser

admin.site.register(MyUser)
admin.site.unregister(Group)
