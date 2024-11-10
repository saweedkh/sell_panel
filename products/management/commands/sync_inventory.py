# Django Built-in modules
from django.core.management.base import BaseCommand

# Local apps
from products.models import Product

# Third Party Apps
from tqdm import tqdm


class Command(BaseCommand):
    help = "Refresh in stock status for products."

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Fetch all products...")
            products = Product.objects.all()
            for product in tqdm(products):
                product.check_in_stock_status()
            self.stdout.write("Done!")
        except Exception as e:
            self.stdout.write(f"Something went wrong!\r\n{e}")
