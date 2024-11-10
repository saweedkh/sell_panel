# Django Built-in modules
from django.db.models import F
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Local apps
from .models import (
    Order,
    OrderItem,
)
from products.models import Warehouse


@receiver(post_save, sender=Order)
def set_warehouse_quantity(sender, instance, created, **kwargs):
    if 'order_status' in instance.changed_fields or created:
        try:
            last_order_status = instance.__last_order_status__
            order_items = instance.orderitem_set.filter(
                product__inventory_management=True
            ).values('variant_id', 'quantity')
            warehouse_transaction_type, possible_status = instance.action_after_status_change(
                old_status=last_order_status,
                new_status=instance.order_status,
            )
            if warehouse_transaction_type == Order.WAREHOUSE_DECREASE:
                Warehouse.decrease_quantity(order_items=order_items)
            elif warehouse_transaction_type == Order.WAREHOUSE_INCREASE:
                Warehouse.increase_quantity(order_items=order_items)
            else:
                pass
        except Order.DoesNotExist:
            return None


@receiver(post_save, sender=Order)
def set_variant_sales(sender, instance, created, **kwargs):
    if 'order_status' in instance.changed_fields or created:
        try:
            last_order_status = instance.__last_order_status__
            warehouse_transaction_type, possible_status = instance.action_after_status_change(
                old_status=last_order_status,
                new_status=instance.order_status,
            )
            for item in instance.orderitem_set.all():
                variant = item.variant
                quantity = item.quantity
                if warehouse_transaction_type == Order.WAREHOUSE_DECREASE:
                    variant.sales = F('sales') + quantity
                elif warehouse_transaction_type == Order.WAREHOUSE_INCREASE:
                    F('sales') - quantity
                variant.save()

        except Order.DoesNotExist:
            return None


@receiver(post_save, sender=Order)
def set_order_values(sender, instance, **kwargs):
    Order.set_province_and_city_in_every_change(instance=instance)
    Order.calculate_prices(instance)


@receiver(pre_save, sender=OrderItem)
def set_order_items_values(sender, instance, **kwargs):
    OrderItem.calculate_price_and_set_values(instance=instance)
