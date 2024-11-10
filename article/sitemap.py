# Django Built-in modules
from django.contrib.sitemaps import Sitemap

# Local apps
from seo.models import AbstractBaseSeoModel
from .models import (
    ArticlePost,
)
from product.models import ProductCategory as ArticleCategory


class ArticleCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ArticleCategory.objects.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).order_by('-created')

    def lastmod(self, obj):
        obj = ArticleCategory.objects.get(pk=obj.id)
        return obj.updated


class ArticlePostsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return ArticlePost.objects.published().order_by('-created')

    def lastmod(self, obj):
        obj = ArticlePost.objects.get(pk=obj.id)
        return obj.updated
