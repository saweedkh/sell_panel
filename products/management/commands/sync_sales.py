# Django Built-in modules
from django.core.management.base import BaseCommand

# Local apps
from order.models import Order
from products.models import Variant

# Third Party Apps
from tqdm import tqdm


class Command(BaseCommand):
    help = "Calculate variant sales count."

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Fetch all variants...")
            for variant in tqdm(Variant.objects.all()):
                sales = 0
                for item in variant.orderitem_set.exclude(
                        order__order_status__in=[Order.AWAITING_PAYMENT, Order.CANCELED, Order.RETURNED]
                ):
                    sales += item.quantity
                variant.sales = sales
                variant.save(update_fields=['sales'])
            self.stdout.write("Done!")
        except Exception as e:
            self.stdout.write(f"Something went wrong!\r\n{e}")
