# Django Built-in modules
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

# Local apps
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel, AbstractContentModel
from .utils import make_automatic_description
from category.models import AbstractBaseCategory

# Third Party Packages
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class CategoryQueryset(models.QuerySet):

    def published(self):
        return self.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).select_related('parent', )


class AbstractBlogCategory(AbstractBaseCategory, AbstractContentModel, AbstractBaseSeoModel, AbstractDateTimeModel):
    short_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('توضیح کوتاه'),
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='categories/%y/%m/%d/',
        verbose_name=_('تصویر'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 60}
    )
    icon = models.ImageField(
        null=True,
        blank=True,
        upload_to='categories/icons/%y/%m/%d/',
        verbose_name=_('آیکون'),
    )
    icon_thumbnail = ImageSpecField(
        source='icon',
        processors=[ResizeToFill(64, 64)],
        format='JPEG',
        options={'quality': 70}
    )

    objects = CategoryQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ('created',)
        unique_together = ('slug', 'parent',)

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _("دسته بندی ها")
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'path': self.get_path()})

    @property
    def default_search_engine_title(self):
        return self.name

    @property
    def default_search_engine_description(self):
        return None

    @property
    def default_search_engine_keywords(self):
        return None

    @property
    def get_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image.url
        except:
            image = static('defaults/default.png')
        return image

    @property
    def get_icon(self):
        try:
            if self.icon.url and self.icon_thumbnail.url and self.icon.file:
                icon = self.icon.url
        except:
            icon = static('defaults/default.png')
        return icon


class PostQueryset(models.QuerySet):

    def published(self):
        return self.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).select_related('author', )


class AbstractBlogPost(AbstractContentModel, AbstractBaseSeoModel, AbstractDateTimeModel):
    author = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('نویسنده'),
    )
    related_blog_item = models.URLField(
        max_length=255,
        verbose_name=_('لینک پست مرتبط'),
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('نام'),
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='posts/%y/%m/%d/',
        verbose_name=_('تصویر'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 400)],
        format='JPEG',
        options={'quality': 60}
    )
    related_posts = models.ManyToManyField(
        'self',
        blank=True,
        through='RelatedPost',
        symmetrical=False,
        verbose_name=_('پست های مرتبط'),
    )
    related_items_display_status = models.BooleanField(
        default=True,
        verbose_name=_('نمایش موارد مرتبط'),
    )
    autofill_related_items = models.BooleanField(
        default=True,
        verbose_name=_('پر کردن خودکار پست های مرتبط'),
    )
    title_image = models.ImageField(
        verbose_name=_('تصویر برای عنوان'),
        null=True,
        blank=True,
        upload_to='posts/%y/%m/%d/title/'
    )
    date_of_news = models.DateField(
        verbose_name=_('تاریخ انتشار'),
        null=True,
        blank=True,
        help_text='اگر انتخاب نشود از تاریخ ایحاد پست استفاده می شود.'
    )
    voice = models.FileField(
        verbose_name=_('صوت'),
        null=True,
        blank=True,
        upload_to='posts/%y/%m/%d/voices/'
    )
    media_text = models.TextField(
        verbose_name=_('متن درمورد فیلم'),
        null=True,
        blank=True
    )
    video_thumbnail = models.ImageField(
        verbose_name=_('تصویر پیش نمایش فیلم'),
        null=True,
        blank=True,
        upload_to='posts/%y/%m/%d/thumbnail/'
    )
    video_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('عنوان ویدیو')
    )
    video = models.URLField(
        verbose_name=_('لینک فیلم'),
        null=True,
        blank=True
    )
    time_to_read = models.PositiveIntegerField(
        verbose_name=_('زمان مطالعه'),
        null=True,
        blank=True,
        default=3,
    )
    views = models.IntegerField(
        default=0,
        verbose_name=_('بازدید'),
    )
    is_important = models.BooleanField(
        default=False,
        verbose_name=_('پست مهم'),
    )
    show_in_head = models.BooleanField(
        default=False,
        verbose_name=_('نمایش در هدر'),
        help_text='پست انتخاب شده در قسمت بالای صفحه نمایش داده می شود.'
    )

    objects = PostQueryset.as_manager()

    class Meta:
        verbose_name = _('پست')
        verbose_name_plural = _('پست ها')
        ordering = ('-created',)
        abstract = True

    def __str__(self):
        return self.name

    @property
    def default_search_engine_title(self):
        return self.name

    @property
    def default_search_engine_description(self):
        return None

    @property
    def default_search_engine_keywords(self):
        return None

    @property
    def get_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image.url
        except:
            image = static('defaults/default.png')
        return image

    @property
    def display_related_items(self):
        setting = AbstractBlogPostSettings.objects.get_first()
        return setting.related_items_display_status and self.related_items_display_status

    def get_short_description(self):
        if not self.description:
            short_description = make_automatic_description(self.content)
            self.description = short_description
            self.save()
        return self.description

    def get_related_posts(self):
        setting = AbstractBlogPostSettings.objects.get_first()
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

            objects = AbstractBlogPost.objects.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).exclude(id__in=id_list)
            result.extend(list(objects)[:remaining])

            return result
        else:
            return related_objects[:num]


class RelatedPost(AbstractDateTimeModel):
    from_post = models.ForeignKey(
        AbstractBlogPost,
        related_name='related_from',
        on_delete=models.CASCADE,
    )
    to_post = models.ForeignKey(
        AbstractBlogPost,
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
        abstract = True

    def __str__(self):
        return str(self.display_priority)


class PostSettingsQueryset(models.QuerySet):
    def get_first(self):
        setting = self.first()
        if not setting:
            setting = self.create()
        return setting


class AbstractBlogPostSettings(AbstractDateTimeModel):
    related_items_display_status = models.BooleanField(
        default=True,
        verbose_name=_('نمایش پست های مرتبط'),
    )
    related_items_number = models.PositiveSmallIntegerField(
        default=10,
        verbose_name=_('تعداد پست های مرتبط'),
    )
    autofill_related_items = models.BooleanField(
        default=True,
        verbose_name=_('پر کردن خودکار پست های مرتبط'),
    )

    objects = PostSettingsQueryset.as_manager()

    class Meta:
        verbose_name = _('پیکربندی پست ها')
        verbose_name_plural = _('پیکربندی پست ها')
        abstract = True

    def __str__(self):
        return str(_('پیکربندی پست ها'))


class BlogTag(AbstractDateTimeModel, AbstractBaseSeoModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('برچسب')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("برچسب")
        verbose_name_plural = _("برچسب ها")
        ordering = ('created',)
        abstract = True
