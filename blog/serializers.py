# # Locals apps
# from .models import AbstractBlogCategory, AbstractBlogPost
# from .translation import (
#     AbstractBlogCategoryTranslationOptions,
#     AbstractBlogPostTranslationOptions,
# )
# from seo.serializers import BaseSeoSerializer, BaseContentSerializer, BaseDateTimeModelSerializer
# from utils.mixins import SerializerTranslationMixin
#
# # Third Party Packages
# from rest_framework import serializers
#
#
# class PostListSerializer(SerializerTranslationMixin, serializers.ModelSerializer):
#     """Get all posts."""
#     author = serializers.CharField(source="author.fullname", read_only=True)
#     # image = serializers.SerializerMethodField()
#
#     class Meta:
#         model = AbstractBlogPost
#         fields = ('pk', 'slug', 'category', 'author', 'name', 'description', 'image',
#                   *BaseDateTimeModelSerializer.Meta.fields,)
#         model_translation = AbstractBlogPostTranslationOptions
#
#     def get_image(self, obj):
#         return obj.get_image
#
#
# class PostDetailSerializer(SerializerTranslationMixin, serializers.ModelSerializer):
#     """Get post detail."""
#     author = serializers.CharField(source="author.fullname", read_only=True)
#     # image = serializers.SerializerMethodField()
#     related_posts = serializers.SerializerMethodField()
#
#     class Meta:
#         model = AbstractBlogPost
#         fields = ('pk', 'category', 'author', 'name', 'image', 'related_posts', *BaseContentSerializer.Meta.fields,
#                   *BaseSeoSerializer.Meta.fields, *BaseDateTimeModelSerializer.Meta.fields,)
#         model_translation = AbstractBlogPostTranslationOptions
#
#     def get_image(self, obj):
#         return obj.get_image
#
#     def get_related_posts(self, obj):
#         if obj.display_related_items:
#             related_posts = obj.get_related_posts()
#             if related_posts:
#                 return related_posts.values('pk', 'slug', 'name', 'image', )
#
#
# class CategoryDetailSerializer(SerializerTranslationMixin, serializers.ModelSerializer):
#     """Get post category detail."""
#     # image = serializers.SerializerMethodField()
#
#     class Meta:
#         model = AbstractBlogCategory
#         fields = ('pk', 'name', 'image', *BaseContentSerializer.Meta.fields, *BaseSeoSerializer.Meta.fields,)
#         model_translation = AbstractBlogCategoryTranslationOptions
#
#     def get_image(self, obj):
#         return obj.get_image
#
#
# class CategoryListSerializer(SerializerTranslationMixin, serializers.ModelSerializer):
#     """Get all post categories."""
#     # image = serializers.SerializerMethodField()
#
#     class Meta:
#         model = AbstractBlogCategory
#         fields = ('pk', 'name', 'image', 'slug',)
#         model_translation = AbstractBlogCategoryTranslationOptions
#
#     def get_image(self, obj):
#         return obj.get_image
