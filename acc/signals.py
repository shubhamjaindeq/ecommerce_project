from django.db.models.signals import post_save
from models import MyUser
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save,sender = MyUser)
def send_email_to_admin(sender,instance,created , **kwargs):
    if created:
        send_mail(
            
        )