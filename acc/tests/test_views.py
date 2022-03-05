import datetime

from django.core import mail
from django.test import TestCase, Client

from allauth.account.admin import EmailAddress

from acc.models import User
from . import user_factory

class CustomerViewsTest(TestCase): 

    def setUp(self):
        self.client = Client()
        self.email= "taviba5898@xindax.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"

    def test_factory(self):
        user = user_factory.UserFactory.create(email = "shubham0109jain@gmail.com")
        user.set_password("shubham@1")
        user.save()
        print(user.password)
        user_factory.UserFactory.create().save()
        user.save()
        c = self.client.login(email = "shubham0109jain@gmail.com", password = self.password1)
        print(c)
        print(User.objects.all())
