"""override and extend django admin behaviour and page"""
from django.contrib import admin
from django.contrib.auth.models import Group

from acc.models import User

admin.site.register(User)
admin.site.unregister(Group)
