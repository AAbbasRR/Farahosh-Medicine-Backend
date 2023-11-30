from django.db.models.signals import post_save
from django.dispatch import receiver

from app_user.models import UserModel


@receiver(post_save, sender=UserModel)
def create_user_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        instance.send_otp_code_to_email("register")
