# django Build-in
# Third Party Packages
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from dynamic_raw_id.admin import DynamicRawIDMixin
from modeltranslation.admin import TabbedTranslationAdmin

from autosave.mixins import AdminAutoSaveMixin
from blog.admin import BlogCategoryAdminMixin, BlogSettingsAdminMixin, BlogTagAdminMixin
# Local Apps
from blog.forms import RelatedPostInlineFormset
from comment.admin import CommentAdminMixin
from .models import Category
from seo.admin import (
    SeoAdminMixin,
    ContentAdminMixin,
)
from utils.admin import DateTimeAdminMixin
from .models import (
    ArticlePostSettings,
    ArticlePost,
    ArticleRelatedPost,
    ArticleComments, ArticleTag
)


@admin.register(Category)
class ArticleCategoryAdmin(BlogCategoryAdminMixin):
    pass

class RelatedPostInline(SortableInlineAdminMixin, DynamicRawIDMixin, admin.TabularInline):
    formset = RelatedPostInlineFormset
    model = ArticleRelatedPost
    fk_name = 'from_post'
    autocomplete_fields = ('to_post',)
    # classes = ('collapse',)
    extra = 0
    ordering = ('display_priority',)


@admin.register(ArticlePost)
class PostAdmin(AdminAutoSaveMixin, SortableAdminBase, DynamicRawIDMixin, TabbedTranslationAdmin):
    fieldsets = (
        (_('پست'), {'fields': (
            'article_type',
            'author',
            'name',
            'title_image',
            'category',
            'time_to_read',
            'date_of_news',
            'image', 'related_blog_item',
            'tag',
            'views',
            'is_important',
            'show_in_head',
        )}),
        (_('مدیا'), {'fields': (
            'media_text',
            'video_title',
            'video_thumbnail',
            'video',
            'voice',
        )}),
        (_('پریمیوم'), {
            # 'classes': ('collapse',),
            'fields': (
                'premium_voice',
                'premium_content',
            )
        }),
        *ContentAdminMixin.fieldsets,
        *SeoAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets,
        (_('تنظیمات بیشتر'), {
            'fields': ('related_items_display_status', 'autofill_related_items'),
            # 'classes': ('collapse',),
        }),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'author',)
    list_display = ('name', *SeoAdminMixin.list_display, 'show_in_head', 'display_post_image_thumbnail')
    list_editable = ('show_in_head',)
    list_per_page = 20
    list_filter = (*SeoAdminMixin.list_filter, 'category', 'show_in_head')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ('category',)
    inlines = (RelatedPostInline, *SeoAdminMixin.inlines,)
    actions = (*SeoAdminMixin.actions,)

    class Media:
        js = (
            "admin/blog/js/make_automatic_description.js",
            "ckeditor/ckeditor/config.js",
        )

    @admin.display(description=_('تصویر'), empty_value='-')
    def display_post_image_thumbnail(self, obj):
        image_url = obj.get_image
        return mark_safe(f'''<a target="_blank" href="{image_url}">
            <img src="{image_url}" class="admin-image-box" width="50" height="50" load="lazy" /></a>''')

    # save current user as author
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
            obj.save()
        super().save_model(request, obj, form, change)


@admin.register(ArticlePostSettings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('display_page_title',)
    fieldsets = (
        *BlogSettingsAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_('تنظیمات'), empty_value='-')
    def display_page_title(self, obj):
        return obj.__str__()


@admin.register(ArticleComments)
class ArticleCommentsAdmin(CommentAdminMixin):
    fieldsets = (
        (_('نظرات'), {
            'fields': (
                'article',
                'parent',
                'user',
                'name',
                'email',
                'review',
                'status',
                'comment_type',
            ),
        }),
    )


@admin.register(ArticleTag)
class ArticleTagAdmin(BlogTagAdminMixin):
    pass
