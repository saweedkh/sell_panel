# Django Build-in
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Local Apps
from blog.models import (
    AbstractBlogPost,
    AbstractBlogPostSettings,
    AbstractBlogCategory, BlogTag
)
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel, AbstractContentModel
from category.models import AbstractBaseCategory
from comment.models import AbstractBaseComment


class Category(AbstractBlogCategory, AbstractBaseSeoModel):
    pass


class ArticlePost(AbstractBlogPost):
    FREE = 0
    PREMIUM = 1
    ARTICLE_STATUS = (
        (FREE, _('عمومی')),
        (PREMIUM, _('آموزشی'))

    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        verbose_name=_('دسته بندی'),
        blank=True,
        null=True,
    )
    related_posts = models.ManyToManyField(
        'self',
        blank=True,
        through='ArticleRelatedPost',
        symmetrical=False,
        verbose_name=_('پست های مرتبط'),
    )
    premium_voice = models.FileField(
        verbose_name=_('صوت ویژه'),
        null=True,
        blank=True,
        upload_to='posts/%y/%m/%d/voices/'
    )
    premium_content = models.TextField(
        verbose_name=_('توضیحات ویژه'),
        null=True,
        blank=True,
    )

    article_type = models.SmallIntegerField(
        choices=ARTICLE_STATUS,
        default=FREE,
        verbose_name=_('نوع مقاله')
    )
    tag = models.ManyToManyField(
        to="ArticleTag",
        blank=True,
        verbose_name=_('برچسب ها'),
        related_name='Tags'
    )

    @property
    def display_related_items(self):
        setting = ArticlePostSettings.objects.get_first()
        return setting.related_items_display_status and self.related_items_display_status

    @property
    def display_related_items(self):
        setting = ArticlePostSettings.objects.get_first()
        return setting.related_items_display_status and self.related_items_display_status

    @property
    def get_related_posts(self):
        setting = ArticlePostSettings.objects.get_first()
        num = setting.related_items_number
        related_objects = self.related_posts.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).order_by(
            'related_to__display_priority')
        if setting.autofill_related_items and self.autofill_related_items:
            result = list(related_objects)
            id_list = [self.id]
            id_list.extend(list(related_objects.values_list('id', flat=True)))
            remaining = num - related_objects.count()

            if remaining > 0:
                return AbstractBlogPost.objects.published().exclude(pk=self.pk).order_by('?')[:remaining]
            else:
                return result[:num]

            objects = ArticlePost.objects.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).exclude(
                id__in=id_list)
            result.extend(list(objects)[:remaining])

            return result
        else:
            return related_objects[:num]

    @property
    def this_is_premium(self):
        if self.article_type == self.PREMIUM:
            return True
        else:
            return False


class ArticleRelatedPost(AbstractDateTimeModel):
    from_post = models.ForeignKey(
        ArticlePost,
        related_name='related_from',
        on_delete=models.CASCADE,
    )
    to_post = models.ForeignKey(
        ArticlePost,
        related_name='related_to',
        verbose_name=_('پست'),
        on_delete=models.CASCADE,
    )
    display_priority = models.PositiveIntegerField(
        db_index=True,
        default=0,
        verbose_name=_('اولویت نمایش'),
    )

    class Meta:
        verbose_name = _("پست مرتبط")
        verbose_name_plural = _("پست های مرتبط")
        ordering = ('display_priority',)

    def __str__(self):
        return str(self.display_priority)


class ArticlePostSettings(AbstractBlogPostSettings):
    pass


class ArticleComments(AbstractBaseComment, AbstractDateTimeModel):
    article = models.ForeignKey(
        ArticlePost,
        verbose_name=_('مقاله'),
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = _('دیدگاه')
        verbose_name_plural = _('دیدگاها')

    def __str__(self):
        return self.name


class ArticleCommentsLikes(AbstractDateTimeModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('کاربر'),
    )
    comment = models.ForeignKey(
        ArticleComments,
        on_delete=models.CASCADE,
        verbose_name=_('دیدگاه')
    )

    class Meta:
        verbose_name = _('لایک')
        verbose_name_plural = _('لایک ها')



class ArticleTag(BlogTag):
    pass

