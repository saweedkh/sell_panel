# Django Built-in modules
from django.db import IntegrityError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

# Local apps
from notification.models import Notification
from .models import User


 
# @receiver(post_save, sender=User)
# def handle_user(sender, instance, **kwargs):
        
#     if kwargs.get('created'): 
#         if instance.type == instance.LEGAL:
#             Notification.create(
#                     user=instance,
#                     text = f'یاد آوری تایید پروفایل',
#                 )