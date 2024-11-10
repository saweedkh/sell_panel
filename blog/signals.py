# Django Built-in modules
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Local apps
from .models import AbstractBlogPost
from .utils import make_automatic_description


@receiver(pre_save, sender=AbstractBlogPost)
def fill_description(sender, instance, **kwargs):
    if instance.content and not instance.description:
        instance.description = make_automatic_description(instance.content)
