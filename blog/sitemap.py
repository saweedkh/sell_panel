# # Django Built-in modules
# from django.contrib.sitemaps import Sitemap
#
# # Local apps
# from seo.models import AbstractBaseSeoModel
# from .models import (
#     AbstractBlogCategory as BlogCategory,
#     AbstractBlogPost,
# )
#
#
# class BlogCategorySitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.8
#     protocol = "https"
#
#     def items(self):
#         return BlogCategory.objects.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).order_by('-created')
#
#     def lastmod(self, obj):
#         obj = BlogCategory.objects.get(pk=obj.id)
#         return obj.updated
#
#
# class BlogPostsSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     protocol = "https"
#
#     def items(self):
#         return AbstractBlogPost.objects.published().order_by('-created')
#
#     def lastmod(self, obj):
#         obj = AbstractBlogPost.objects.get(pk=obj.id)
#         return obj.updated
