# Django Built-in modules
from django.core.management.base import BaseCommand

# Local apps
from products.models import Product


class Command(BaseCommand):
    help = "Add the ancestors of products' current categories to their categories."

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Fetch all products...")
            products = Product.objects.all()
            for product in products:
                categories = product.category.all()
                for category in categories:
                    ancestors = category.get_ancestors()
                    if len(ancestors) != 0:
                        id_list = ancestors.values_list('id', flat=True)
                        product.category.add(*id_list)
                        product.save()
            self.stdout.write("Done!")
        except Exception as e:
            self.stdout.write(f"Something went wrong!\r\n{e}")
