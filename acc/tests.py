"""design and run tests for your appliaction"""
import hashlib
import datetime

from django.core import mail
from django.test import TestCase, Client

print(len(mail.outbox))


from allauth.account.admin import EmailAddress

from.models import User

class CustomerAuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.email= "hedoca5169@zneep.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "http://testserver/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"

    def test_create_user_as_customer(self):
        user = User.objects.create_user(
            full_name = "Shubham Jain",
            date_of_birth = datetime.date.today(),
            email = "hedoca5169@zneep.com",
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
            "next" : "/",
        })
        #print(mail.outbox[0].body)
        verify_response = self.client.post(self.verifyurl, data={})
        self.assertEqual(verify_response.status_code, 302)
        self.assertEqual(True, EmailAddress.objects.get(email = self.email).verified)

    def test_login(self):

        response = self.client.post("/accounts/signup/", data={
            'email': "shubham0109jain@gmail.com",
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': "shubham@1",
            'password2': "shubham@1",
            "next" : "/",
        })
        #print(response)
        #print(mail.outbox[0].body)
        url = "/accounts/confirm-email/MQ:1nQ0hf:_pXHKfp1eJV3_0dON38uvTgAnM6FGCxpxscTJNUFCuQ/"
        verify_response = self.client.post(url, data={})
        #print(verify_response)
        login_response = self.client.get(verify_response.url)
        self.assertTemplateUsed(login_response, template_name="account/login.html")
        users = User.objects.all()
        print(users)
        emails = EmailAddress.objects.all()
        print(emails[0].verified)
        login_req = self.client.post("/accounts/login/", data = {
            'login': "shubham0109jain@gmail.com",
            'password': "shubham@1",
            
        } )
        #print(login_req , "is response")
        response = self.client.get("")
        #print(response)
        #HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        
        #self.assertTemplateUsed(login_req, template_name="account/login.html")
        user = User.objects.get(id=1)
        #print(user.password)
        


    
        