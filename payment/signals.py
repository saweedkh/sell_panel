# Django Built-in modules
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local apps
from .models import Receipt
from orders.models import Order


@receiver(post_save, sender=Receipt)
def confirm_bank_receipt(sender, instance, **kwargs):
    if instance.status == instance.ACCEPTED:
        instance.order.complete_the_order(payment_method=Order.TRANSFER)
