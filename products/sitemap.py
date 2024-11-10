# Django Built-in modules
from django.contrib.sitemaps import Sitemap

# Local apps
from seo.models import AbstractBaseSeoModel
from .models import (
    Category as ProductCategory,
    ProductList,
    Product,
    Brand,
)


class ProductCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ProductCategory.objects.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).order_by('-created')

    def lastmod(self, obj):
        obj = ProductCategory.objects.get(pk=obj.id)
        return obj.updated


class ProductListSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ProductList.objects.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).order_by('-created')

    def lastmod(self, obj):
        obj = ProductList.objects.get(pk=obj.id)
        return obj.updated


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return Product.objects.published().order_by('-created')

    def lastmod(self, obj):
        obj = Product.objects.get(pk=obj.id)
        return obj.updated


class ProductBrandSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return Brand.objects.published().order_by('-created')

    def lastmod(self, obj):
        obj = Brand.objects.get(pk=obj.id)
        return obj.updated
