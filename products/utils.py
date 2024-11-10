# django built-in modules
from django.db.models import TextChoices, Subquery, OuterRef, F, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.utils.text import Truncator

# Third party packages
from bs4 import BeautifulSoup



class ProductSortChoices(TextChoices):
    NEWEST = 'date-desc', _('جدیدترین')
    OLDEST = 'date-asc', _('قدیمی ترین')
    MOST_EXPENSIVE = 'price-desc', _('گران ترین')
    CHEAPEST = 'price-asc', _('ارزان ترین')
    BEST_SELLING = 'sale', _('پرفروش ترین')


def sort_products(sort_param, default, qs):
    Variant = apps.get_model('products', 'Variant')

    if not sort_param:
        sort_param = default

    if sort_param == ProductSortChoices.NEWEST:
        return qs.order_by('-in_stock', '-created')

    elif sort_param == ProductSortChoices.OLDEST:
        return qs.order_by('-in_stock', 'created')

    elif sort_param == ProductSortChoices.MOST_EXPENSIVE:
        return qs.annotate(
            default_price=Subquery(
                Variant.objects.filter(
                    product_id=OuterRef('pk')
                ).annotate(
                    total_price=F('price') - Coalesce(F('discount'), 0)
                ).order_by(
                    '-in_stock',
                    '-default',
                    'total_price'
                ).values_list('total_price', flat=True)[:1],
            )
        ).order_by('-in_stock', '-default_price')

    elif sort_param == ProductSortChoices.CHEAPEST:
        return qs.annotate(
            default_price=Subquery(
                Variant.objects.filter(
                    product_id=OuterRef('pk')
                ).annotate(
                    total_price=F('price') - Coalesce(F('discount'), 0)
                ).order_by(
                    '-in_stock',
                    '-default',
                    'total_price'
                ).values_list('total_price', flat=True)[:1],
            )
        ).order_by('-in_stock', 'default_price')

    elif sort_param == ProductSortChoices.BEST_SELLING:
        return qs.annotate(sales=Sum("variant__sales")).order_by('-in_stock', '-sales')

    else:
        return qs





def make_automatic_description(content):
    soup = BeautifulSoup(content, "html.parser")
    paragraphs = soup.find_all(['p', ])
    if paragraphs:
        for paragraph in paragraphs:
            content = paragraph.get_text()
            if content != '':
                return Truncator(content).words(30)
    content = soup.get_text()
    return Truncator(content).words(30)
