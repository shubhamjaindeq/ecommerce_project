"""override and extend django admin behaviour and page"""
from django.contrib import admin
from django.contrib.auth.models import Group

from acc.models import User ,Product

admin.site.register(User)
admin.site.register(Product)

admin.site.unregister(Group)
