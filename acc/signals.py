
from django.dispatch import receiver
from django.shortcuts import render
from django.template.loader import render_to_string# code
from django.db.models.signals import post_save, pre_delete

from .models import MyUser
from django.core.mail import send_mail



@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        id = instance.id
        if instance.role == "shopowner":
            instance.changeactive(False)
            
            a = instance.password
            instance.passchange(a)
            val = {'id': id}
            messagestring = "http://127.0.0.1:8000/acc/approval/" + str(val['id'])
            
            send_mail("hi This person wants to register", messagestring, "codetestbyshubham@gmail.com",["shujain@deqode.com"])
