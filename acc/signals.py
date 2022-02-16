from django.template.loader import render_to_string# code
from django.db.models.signals import post_save, pre_delete
# from django.contrib.auth.models import MyUser
from django.dispatch import receiver
from .models import MyUser
from django.core.mail import send_mail



@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        #MyUser.objects.create()
        id = instance.id
        #print(id)
        print(instance.role,"is your instance role")
        #print(instance.gender)
        if instance.role == "shopowner":
            instance.changeactive(False)
            print(instance.password)
            a = instance.password
            instance.passchange(a)
            val = {'id': id}
            msg_html = render_to_string('profile.html' , val)

            send_mail("hi This person wants to register", "yoooooo", "codetestbyshubham@gmail.com",["shujain@deqode.com"],html_message=msg_html)

            print("created")


