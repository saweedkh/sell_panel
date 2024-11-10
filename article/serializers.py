# Django Build-in
from django.http import HttpRequest
# Third Party Packages
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from account.models import User
from seo.serializers import (
    BaseDateTimeModelSerializer,
    BaseSeoSerializer,
    BaseContentSerializer
)
from utils.jdatetime import standard_jalali_date_format
from utils.serializers import CustomModelSerializers as ModelSerializer
# Local Apps
from .models import ArticlePost, ArticleComments, ArticleCommentsLikes, ArticleTag, Category
from .translation import ArticlePostTranslationOptions, ArticleTagTranslationOptions



class CategoryListSerializers(ModelSerializer):
    """Get all categories."""

    class Meta:
        model = Category

        fields = (
            'pk', 'name', 'image', 'slug', 'short_description',
        )



class CategoryDetailSerializers(ModelSerializer, BaseSeoSerializer):
    """Get category detail."""

    class Meta:
        model = Category
        fields = ('pk', 'name', 'image', 'slug', 'short_description', *BaseSeoSerializer.Meta.fields,)

class ArticleTagSerializers(ModelSerializer, BaseDateTimeModelSerializer):
    """return a Tag"""

    class Meta:
        model = ArticleTag
        fields = (
            'pk',
            'name',
            *BaseSeoSerializer.Meta.fields
        )
        model_translation = ArticleTagTranslationOptions


class ArticlePostSerializers(ModelSerializer, BaseDateTimeModelSerializer):
    """Get all post articles.""",
    author = serializers.CharField(source="author.fullname", read_only=True)
    category = serializers.CharField(source="category.slug", read_only=True)

    class Meta:
        model = ArticlePost
        fields = (
            'pk', 'slug', 'author', 'category', 'name', 'description', 'title_image', 'views', 'is_important',
            'date_of_news', 'article_type',
            *BaseDateTimeModelSerializer.Meta.fields,)
        model_translation = ArticlePostTranslationOptions

    def get_image(self, obj):
        return obj.get_image


class ArticlePostDetailSerializers(ModelSerializer, BaseSeoSerializer, BaseDateTimeModelSerializer):
    """Get article detail."""

    def __init__(self, *args, **kwargs):
        super(ArticlePostDetailSerializers, self).__init__(*args, **kwargs)
        self.request: HttpRequest = self.context.get('request')

    author = serializers.CharField(source="author.fullname", read_only=True)
    category = serializers.CharField(source="category.slug", read_only=True)
    related_posts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    voice = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    media_text = serializers.SerializerMethodField()
    video_thumbnail = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    tag = ArticleTagSerializers(read_only=True, many=True)

    class Meta:
        model = ArticlePost
        fields = (
            'pk', 'category', 'author', 'name', 'image', 'time_to_read', 'voice', 'description', 'content',
            'media_text',
            'video_title', 'video_thumbnail', 'video', 'views', 'is_important', 'related_posts', 'date_of_news',
            'article_type',
            'tag',
            'comments',
            *BaseContentSerializer.Meta.fields,
            *BaseSeoSerializer.Meta.fields, *BaseDateTimeModelSerializer.Meta.fields,)
        model_translation = ArticlePostTranslationOptions

    def get_image(self, obj):
        return obj.get_image

    @extend_schema_field(list)
    def get_related_posts(self, obj):
        return ArticlePostSerializers(instance=ArticlePost.objects.published().filter(category=obj.category),
                                      many=True).data

    @extend_schema_field(list)
    def get_comments(self, obj):
        return ArticleCommentsSerializers(
            instance=ArticleComments.objects.filter(article=obj.id, status=ArticleComments.ACCEPT), many=True).data

    @extend_schema_field(str)
    def get_voice(self, obj):
        if obj.this_is_premium and not self.request.user.is_authenticated:
            if obj.voice:
                return obj.voice.url

        else:
            if obj.premium_voice:
                return obj.premium_voice.url
            if obj.voice:
                return obj.voice.url
            return None

    @extend_schema_field(str)
    def get_content(self, obj):
        if obj.this_is_premium and not self.request.user.is_authenticated:
            return obj.content
        else:
            return obj.premium_content

    @extend_schema_field(str)
    def get_description(self, obj):
        if obj.this_is_premium and not self.request.user.is_authenticated:
            return obj.description
        else:
            return obj.description

    @extend_schema_field(str)
    def get_media_text(self, obj):
        if obj.this_is_premium and not self.request.user.is_authenticated:
            return None
        else:
            return obj.media_text

    @extend_schema_field(str)
    def get_video_thumbnail(self, obj):
        if obj.this_is_premium and not self.request.user.is_authenticated:
            if obj.video_thumbnail:
                return obj.video_thumbnail.url
            return None
        else:
            if obj.video_thumbnail:
                return obj.video_thumbnail.url
            return None

    @extend_schema_field(str)
    def get_video(self, obj):
        if obj.this_is_premium and not self.request.user.is_authenticated:
            return None
        else:
            return obj.video


class ArticleCommentsSerializers(ModelSerializer, BaseDateTimeModelSerializer):
    """Get all comments"""
    likes = serializers.SerializerMethodField()
    jcreated = serializers.SerializerMethodField()

    class Meta:
        model = ArticleComments
        fields = (
            'article',
            'parent',
            'user',
            'name',
            'email',
            'review',
            'status',
            'likes',
            *BaseDateTimeModelSerializer.Meta.fields,
        )
        model_translation = ArticlePostTranslationOptions

    @extend_schema_field(int)
    def get_likes(self, obj):
        return ArticleCommentsLikes.objects.filter(comment_id=obj.id).count()

    @extend_schema_field(str)
    def get_jcreated(self, obj):
        return standard_jalali_date_format(obj.created)


class ArticleCreateCommentsSerializers(ModelSerializer, BaseDateTimeModelSerializer):
    """Create Comments."""
    captcha = serializers.CharField(max_length=100)
    key = serializers.CharField(max_length=255)

    # captcha = CaptchaField()

    class Meta:
        model = ArticleComments
        fields = (
            'article',
            'parent',
            'name',
            'review',
            'captcha',
            'key',
            *BaseDateTimeModelSerializer.Meta.fields,
        )
        model_translation = ArticlePostTranslationOptions

    def create(self, validated_data):
        if validated_data.get('captcha'):
            del validated_data['captcha']
        if validated_data.get('key'):
            del validated_data['key']

        user: User = self.context['request'].user
        if user.is_authenticated:
            comment: ArticleComments = ArticleComments.objects.create(
                article=validated_data['article'],
                parent=validated_data['parent'],
                user=user,
                name=user.first_name,
                email=user.email,
                review=validated_data['review'],
            )
        else:
            comment: ArticleComments = ArticleComments.objects.create(
                article=validated_data['article'],
                parent=validated_data['parent'],
                name=validated_data['name'],
                email=validated_data['email'],
                review=validated_data['review'],
            )

        return comment


class ArticleCommentLikesSerializers(ModelSerializer, BaseDateTimeModelSerializer):
    """Like a Comment"""

    class Meta:
        model = ArticleCommentsLikes
        fields = ('user', 'comment')
        model_translation = ArticlePostTranslationOptions
