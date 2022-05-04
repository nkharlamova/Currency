from accounts.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def pre_save_user_last_name_change(sender, instance, **kwargs):
    if instance.last_name:
        instance.last_name = instance.last_name.capitalize()


@receiver(pre_save, sender=User)
def pre_save_user_first_name_change(sender, instance, **kwargs):
    if instance.first_name:
        instance.first_name = instance.first_name.capitalize()


@receiver(pre_save, sender=User)
def user_pre_save_phone_field(sender, instance, **kwargs):
    if instance.phone:
        instance.phone = ''.join([element for element in instance.phone if element.isdigit()])


@receiver(pre_save, sender=User)
def user_pre_save_email_field(sender, instance, **kwargs):
    if instance.email:
        instance.email = instance.email.lower()
