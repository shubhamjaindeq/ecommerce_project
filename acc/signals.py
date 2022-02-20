
import pdb
from django.dispatch import receiver
from django.shortcuts import render
from django.template.loader import render_to_string# code
from django.db.models.signals import post_save, pre_delete

from .models import User
from django.core.mail import send_mail

from allauth.account.signals import user_signed_up, email_confirmed

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    print("signal called")
    breakpoint()
    new_email_address = email_address
    user = User.objects.get(email = new_email_address)
    if user.role == "shopowner":
        user.is_active = False
        user.save()
        messagestring = "http://127.0.0.1:8000/approval/" + str(user.id)
        send_mail("hi This person wants to register", messagestring, "codetestbyshubham@gmail.com",["shujain@deqode.com"])
    print("email confirmation signal called",new_email_address , user)