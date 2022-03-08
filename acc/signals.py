"""Signals to call after and before events in the application"""
from django.dispatch import receiver
from django.core.mail import send_mail

from allauth.account.signals import email_confirmed

from .models import User


@receiver(email_confirmed)
def email_confirmed_(email_address, **kwargs):
    """sends approval mail for shopowners"""

    new_email_address = email_address
    user = User.objects.get(email = new_email_address)
    if user.role == "shopowner":
        user.is_active = False
        user.save()
        messagestring = "http://127.0.0.1:8000/acc/approval/" + str(user.id)
        send_mail("hi This person wants to register", messagestring,
        "codetestbyshubham@gmail.com",["shujain@deqode.com"])
