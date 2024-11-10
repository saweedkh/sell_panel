# Django Built-in modules
from django.db.models.signals import pre_save, m2m_changed, post_save, post_delete
from django.db import transaction
from django.dispatch import receiver

# Local apps
from .models import (
    Variant,
    AttributeValue,
    ProductComment as Comment,
    Attribute,
    Product,
    Warehouse,
)


@receiver(post_save, sender=Product)
def change_in_stock_status_in_variant_level(sender, instance, **kwargs):
    if 'type' in instance.changed_fields:
        instance.in_stock = instance.check_in_stock_status(automatic_status_update=False)


@receiver(post_save, sender=Variant)
def change_in_stock_status_in_variant_level(sender, instance, **kwargs):
    if hasattr(instance, 'dry_run') and getattr(instance, 'dry_run'):
        return
    if 'in_stock' in instance.changed_fields:
        instance.product.check_in_stock_status()


@receiver(post_save, sender=Warehouse)
def change_in_stock_status_in_warehouse_level(sender, instance, **kwargs):
    if hasattr(instance, 'dry_run') and getattr(instance, 'dry_run'):
        return            
    instance.product.check_in_stock_status()


@receiver(pre_save, sender=AttributeValue)
def set_attribute_name_for_attribute_value(sender, instance, **kwargs):
    instance.attribute_name = instance.attribute.name


@receiver(post_save, sender=Attribute)
def change_attribute_name_in_attribute_value_if_attribute_name_changed(sender, instance, **kwargs):
    if instance.track_fields_for_signal():
        instance.attributevalue_set.update(attribute_name=instance.name)


@receiver(m2m_changed, sender=Variant.attribute_values.through)
def attribute_values_changed_in_variant(sender, instance, **kwargs):
    for variant in Variant.objects.filter(product_id=instance.product_id).prefetch_related('attribute_values', ):
        attribute_values = variant.attribute_values.all()
        if attribute_values:
            variant.variant_name = ' | '.join([f"{item.attribute_name}: {item.name}" for item in attribute_values])
            variant.save()


@receiver(post_save, sender=Product)
def set_warehouse_record_for_inventory_management(sender, instance, **kwargs):
    if 'inventory_management' in instance.changed_fields:
        if instance.inventory_management:
            Warehouse.create_records(variants=instance.variant_set.all())
        else:
            Warehouse.delete_records(product_id=instance.id)


@receiver(post_save, sender=Variant)
def set_warehouse_record_for_inventory_management2(sender, instance, created, **kwargs):
    if hasattr(instance, 'dry_run') and getattr(instance, 'dry_run'):
        return
    if created and instance.product.inventory_management:
        Warehouse.create_records(variants=[instance, ])


@receiver(post_delete, sender=Variant)
def set_warehouse_record_for_inventory_management3(sender, instance, **kwargs):
    if hasattr(instance, 'dry_run') and getattr(instance, 'dry_run'):
        return
    if instance.product.inventory_management:
        Warehouse.delete_single_records(variant_id=instance.pk)


def update_variants_product_name_field(instance):
    instance.variant_set.update(product_name=instance.name)


@receiver(pre_save, sender=Product)
def set_variation_name_for_variant(sender, instance, **kwargs):
    if instance.track_fields_for_signal():
        transaction.on_commit(
            lambda: update_variants_product_name_field(instance)
        )


@receiver(pre_save, sender=Variant)
def set_product_name_for_variant(sender, instance, **kwargs):
    if hasattr(instance, 'dry_run') and getattr(instance, 'dry_run'):
        return
    if not instance.product_name:
        instance.product_name = instance.product.name
