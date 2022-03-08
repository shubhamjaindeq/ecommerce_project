"""design and run tests for your appliaction"""
import datetime

from django.core import mail
from django.test import TestCase, Client
from allauth.account.admin import EmailAddress

from acc.models import User

class CustomerAuthTest(TestCase):

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
        self.verifyurl = "/accounts/confirm-email/MQ:1nRATj:tcN5EBIkmoC9sAy1ZdNNgpYU4A_XgpcGqD5DiWNGEG8/"

    def test_create_user_as_customer(self):
        user = User.objects.create_user(
            full_name = "Shubham Jain",
            date_of_birth = datetime.date.today(),
            email = self.email,
            gender = "male",
            address = "123 Main street",
            role = "customer",
            password = "shubham@1"
        )
        resp_user = User.objects.get(id=user.id)
        self.assertEqual(user, resp_user)
        self.assertEqual(user.shopname, None)

    def test_signup_page_url(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/signup.html')

    def test_signup(self):
        response = self.client.post("/accounts/signup/", data={
            'email': self.email,
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
            "next" : "/",
        })
        self.assertEqual(response.status_code, 302)
        redirect_to = self.client.get(response.url)
        self.assertTemplateUsed(redirect_to, template_name = "account/verification_sent.html")
        users = User.objects.all()
        self.assertEqual(users.count(), 1) 
        self.assertFalse(EmailAddress.objects.get(email = self.email).verified)

    def test_signup_fail(self):
        response = self.client.post("/accounts/signup/", data={
            'email': self.email,
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': "abcd",
            'password2': self.password2,
            "next" : "/",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = "account/signup.html")

    def test_email_confirm(self):
        response = self.client.post("/accounts/signup/", data={
            'email': self.email,
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
        })
        verify_response = self.client.post(self.verifyurl, data={})
        self.assertEqual(verify_response.status_code, 302)
        self.assertEqual(True, EmailAddress.objects.get(email = self.email).verified)

    def test_login(self):

        response = self.client.post("/accounts/signup/", data={
            'email': self.email,
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
        })
        verify_response = self.client.post(self.verifyurl, data={})
        login_response = self.client.get(verify_response.url)
        self.assertTemplateUsed(login_response, template_name="account/login.html")
        login_req = self.client.post("/accounts/login/", data = {
            'login': self.email,
            'password': self.password1,
        } )
        response = self.client.get(login_req.url)
        user = User.objects.get(id=1)
        self.assertEqual(user.is_authenticated, True)
        self.assertTemplateUsed(response, template_name="customer/customerindex.html")
        
        
    def test_login_fail(self):

        response = self.client.post("/accounts/signup/", data={
            'email': self.email,
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
            "next" : "/",
        })
        verify_response = self.client.post(self.verifyurl, data={})
        login_response = self.client.get(verify_response.url)
        self.assertTemplateUsed(login_response, template_name="account/login.html")
        login_req = self.client.post("/accounts/login/", data = {
            'login': self.email,
            'password': "abcd",
        } )
        self.assertTemplateUsed(login_req, template_name="account/login.html")

class AdminAuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.email= "shujain@deqode.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "root"
        self.password2 = "root"

    def test_create_superuser(self):

        User.objects.create_superuser(
            full_name = "Shubham Jain",
            date_of_birth = datetime.date.today(),
            email = self.email,
            gender = "male",
            address = "123 Main street",
            role = "admin",
            password = self.password1,
        )
        self.client.login(email = self.email, password=self.password1)
        user = User.objects.get(email = self.email)
        self.assertEqual(user.is_authenticated, True)


class ShopAuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.email= "taviba5898@xindax.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.shopname = "Bata centre"
        self.shopdesc = "A place for all your feet needs"
        self.shopaddress = "Indore"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nRATj:tcN5EBIkmoC9sAy1ZdNNgpYU4A_XgpcGqD5DiWNGEG8/"

    def test_create_user_as_shop(self):
        user = User.objects.create_user(
            full_name = "Shubham Jain",
            date_of_birth = datetime.date.today(),
            email = "hedoca5169@zneep.com",
            gender = "male",
            address = "123 Main street",
            role = "customer",
            password = "shubham@1",
            shopname = self.shopname,
            shopaddress = self.shopaddress,
            shopdesc = self.shopdesc
        )
        resp_user = User.objects.get(id=user.id)
        self.assertEqual(user, resp_user)
        self.assertEqual(user.shopname, self.shopname)

    def test_signup_page_url(self):
        response = self.client.get("/acc/signupasshop/")
        self.assertTemplateUsed(response, template_name="account/shopsignup.html")

    def test_signup_as_shop(self):
        User.objects.create_superuser(
            full_name = "Shubham Jain",
            date_of_birth = datetime.date.today(),
            email = "shujain@deqode.com",
            gender = "male",
            address = "123 Main street",
            role = "admin",
            password = "root",
        )
        response = self.client.post("/acc/signupasshop/", data={
            'email': self.email,
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
            "next" : "/",
            "shopname" : self.shopname,
            "shopaddress" : self.shopaddress,
            "shopdesc": self.shopdesc,
        })
        login_req = self.client.post("/accounts/login/", data = {
            'login': self.email,
            'password': self.password1,
        } )
        verify_response = self.client.post(self.verifyurl, data={})
        self.assertFalse(User.objects.get(email = self.email).is_active)
        user = User.objects.get(email = self.email)
        user.is_active = True
        user.save()
        result = self.client.login(email = self.email, password = self.password1)
        self.assert_(result)

    def test_login(self):

        self.client.post("/acc/signupasshop/", data={
            'email': self.email,
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
            "next" : "/",
            "shopname" : self.shopname,
            "shopaddress" : self.shopaddress,
            "shopdesc": self.shopdesc,
        })
        login_req = self.client.post("/accounts/login/", data = {
            'login': self.email,
            'password': self.password1,
        } )
        verify_response = self.client.post(self.verifyurl, data={})
        user = User.objects.get(email = self.email)
        user.is_active = True
        user.save()
        login_req = self.client.post("/accounts/login/", data = {
            'login': self.email,
            'password': self.password1,
        } )
        response = self.client.get(login_req.url)
        user = User.objects.get(email = self.email)
        self.assertEqual(user.is_authenticated, True)
        self.assertTemplateUsed(response, template_name="shop/shopindex.html")
