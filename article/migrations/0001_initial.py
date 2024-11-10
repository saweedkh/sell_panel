# Generated by Django 4.2.16 on 2024-11-10 07:43

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('review', models.TextField(max_length=400, verbose_name='متن دیدگاه')),
                ('status', models.SmallIntegerField(choices=[(0, 'در صف'), (1, 'پذیرش'), (2, 'رد')], default=0, verbose_name='وضعیت')),
                ('comment_type', models.SmallIntegerField(choices=[(0, 'نظر'), (1, 'پرسش و پاسخ')], default=0, verbose_name='نوع')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'دیدگاه',
                'verbose_name_plural': 'دیدگاها',
            },
        ),
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True, verbose_name='اسلاگ')),
                ('slug_fa', models.SlugField(allow_unicode=True, max_length=255, null=True, unique=True, verbose_name='اسلاگ')),
                ('slug_en', models.SlugField(allow_unicode=True, max_length=255, null=True, unique=True, verbose_name='اسلاگ')),
                ('page_display_status', models.SmallIntegerField(choices=[(0, 'پیش نویس'), (1, 'انتشار')], default=0, verbose_name='وضعیت نمایش صفحه')),
                ('search_engine_title', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_title_fa', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_title_en', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_description', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_description_fa', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_description_en', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_keywords', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('search_engine_keywords_fa', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('search_engine_keywords_en', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('canonical_link', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('canonical_link_fa', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('canonical_link_en', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('description_fa', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='محتوا')),
                ('content_fa', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='محتوا')),
                ('content_en', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='محتوا')),
                ('related_blog_item', models.URLField(blank=True, max_length=255, null=True, verbose_name='لینک پست مرتبط')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='نام')),
                ('name_fa', models.CharField(max_length=255, null=True, unique=True, verbose_name='نام')),
                ('name_en', models.CharField(max_length=255, null=True, unique=True, verbose_name='نام')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/%y/%m/%d/', verbose_name='تصویر')),
                ('image_fa', models.ImageField(blank=True, null=True, upload_to='posts/%y/%m/%d/', verbose_name='تصویر')),
                ('image_en', models.ImageField(blank=True, null=True, upload_to='posts/%y/%m/%d/', verbose_name='تصویر')),
                ('related_items_display_status', models.BooleanField(default=True, verbose_name='نمایش موارد مرتبط')),
                ('autofill_related_items', models.BooleanField(default=True, verbose_name='پر کردن خودکار پست های مرتبط')),
                ('title_image', models.ImageField(blank=True, null=True, upload_to='posts/%y/%m/%d/title/', verbose_name='تصویر برای عنوان')),
                ('date_of_news', models.DateField(blank=True, help_text='اگر انتخاب نشود از تاریخ ایحاد پست استفاده می شود.', null=True, verbose_name='تاریخ انتشار')),
                ('voice', models.FileField(blank=True, null=True, upload_to='posts/%y/%m/%d/voices/', verbose_name='صوت')),
                ('media_text', models.TextField(blank=True, null=True, verbose_name='متن درمورد فیلم')),
                ('media_text_fa', models.TextField(blank=True, null=True, verbose_name='متن درمورد فیلم')),
                ('media_text_en', models.TextField(blank=True, null=True, verbose_name='متن درمورد فیلم')),
                ('video_thumbnail', models.ImageField(blank=True, null=True, upload_to='posts/%y/%m/%d/thumbnail/', verbose_name='تصویر پیش نمایش فیلم')),
                ('video_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='عنوان ویدیو')),
                ('video_title_fa', models.CharField(blank=True, max_length=255, null=True, verbose_name='عنوان ویدیو')),
                ('video_title_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='عنوان ویدیو')),
                ('video', models.URLField(blank=True, null=True, verbose_name='لینک فیلم')),
                ('time_to_read', models.PositiveIntegerField(blank=True, default=3, null=True, verbose_name='زمان مطالعه')),
                ('views', models.IntegerField(default=0, verbose_name='بازدید')),
                ('is_important', models.BooleanField(default=False, verbose_name='پست مهم')),
                ('show_in_head', models.BooleanField(default=False, help_text='پست انتخاب شده در قسمت بالای صفحه نمایش داده می شود.', verbose_name='نمایش در هدر')),
                ('premium_voice', models.FileField(blank=True, null=True, upload_to='posts/%y/%m/%d/voices/', verbose_name='صوت ویژه')),
                ('premium_voice_fa', models.FileField(blank=True, null=True, upload_to='posts/%y/%m/%d/voices/', verbose_name='صوت ویژه')),
                ('premium_voice_en', models.FileField(blank=True, null=True, upload_to='posts/%y/%m/%d/voices/', verbose_name='صوت ویژه')),
                ('premium_content', models.TextField(blank=True, null=True, verbose_name='توضیحات ویژه')),
                ('premium_content_fa', models.TextField(blank=True, null=True, verbose_name='توضیحات ویژه')),
                ('premium_content_en', models.TextField(blank=True, null=True, verbose_name='توضیحات ویژه')),
                ('article_type', models.SmallIntegerField(choices=[(0, 'عمومی'), (1, 'آموزشی')], default=0, verbose_name='نوع مقاله')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست ها',
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticlePostSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('related_items_display_status', models.BooleanField(default=True, verbose_name='نمایش پست های مرتبط')),
                ('related_items_number', models.PositiveSmallIntegerField(default=10, verbose_name='تعداد پست های مرتبط')),
                ('autofill_related_items', models.BooleanField(default=True, verbose_name='پر کردن خودکار پست های مرتبط')),
            ],
            options={
                'verbose_name': 'پیکربندی پست ها',
                'verbose_name_plural': 'پیکربندی پست ها',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True, verbose_name='اسلاگ')),
                ('slug_fa', models.SlugField(allow_unicode=True, max_length=255, null=True, unique=True, verbose_name='اسلاگ')),
                ('slug_en', models.SlugField(allow_unicode=True, max_length=255, null=True, unique=True, verbose_name='اسلاگ')),
                ('page_display_status', models.SmallIntegerField(choices=[(0, 'پیش نویس'), (1, 'انتشار')], default=0, verbose_name='وضعیت نمایش صفحه')),
                ('search_engine_title', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_title_fa', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_title_en', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_description', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_description_fa', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_description_en', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_keywords', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('search_engine_keywords_fa', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('search_engine_keywords_en', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('canonical_link', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('canonical_link_fa', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('canonical_link_en', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('name', models.CharField(max_length=255, verbose_name='برچسب')),
                ('name_fa', models.CharField(max_length=255, null=True, verbose_name='برچسب')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='برچسب')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
                'ordering': ('created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('name_fa', models.CharField(max_length=255, null=True, verbose_name='نام')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True, verbose_name='اسلاگ')),
                ('slug_fa', models.SlugField(allow_unicode=True, max_length=255, null=True, unique=True, verbose_name='اسلاگ')),
                ('slug_en', models.SlugField(allow_unicode=True, max_length=255, null=True, unique=True, verbose_name='اسلاگ')),
                ('page_display_status', models.SmallIntegerField(choices=[(0, 'پیش نویس'), (1, 'انتشار')], default=0, verbose_name='وضعیت نمایش صفحه')),
                ('search_engine_title', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_title_fa', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_title_en', models.CharField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', max_length=255, null=True, verbose_name='عنوان موتور جستجو')),
                ('search_engine_description', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_description_fa', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_description_en', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='توضیحات موتور جستجو')),
                ('search_engine_keywords', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('search_engine_keywords_fa', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('search_engine_keywords_en', models.TextField(blank=True, help_text='اگر خالی باشد، پیش نمایش آنچه را که به طور خودکار تولید می شود نشان می دهد.', null=True, verbose_name='کلید واژه های موتور جستجو')),
                ('canonical_link', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('canonical_link_fa', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('canonical_link_en', models.URLField(blank=True, help_text='تگ های کنونیکال به مشکلات محتوای تکراری کمک می کنند.', null=True, verbose_name='لینک کنونیکال')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('description_fa', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='محتوا')),
                ('content_fa', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='محتوا')),
                ('content_en', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='محتوا')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='توضیح کوتاه')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/%y/%m/%d/', verbose_name='تصویر')),
                ('image_fa', models.ImageField(blank=True, null=True, upload_to='categories/%y/%m/%d/', verbose_name='تصویر')),
                ('image_en', models.ImageField(blank=True, null=True, upload_to='categories/%y/%m/%d/', verbose_name='تصویر')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='categories/icons/%y/%m/%d/', verbose_name='آیکون')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='article.category', verbose_name='والد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'abstract': False,
            },
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ArticleRelatedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('display_priority', models.PositiveIntegerField(db_index=True, default=0, verbose_name='اولویت نمایش')),
                ('from_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_from', to='article.articlepost')),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_to', to='article.articlepost', verbose_name='پست')),
            ],
            options={
                'verbose_name': 'پست مرتبط',
                'verbose_name_plural': 'پست های مرتبط',
                'ordering': ('display_priority',),
            },
        ),
        migrations.AddField(
            model_name='articlepost',
            name='related_posts',
            field=models.ManyToManyField(blank=True, through='article.ArticleRelatedPost', to='article.articlepost', verbose_name='پست های مرتبط'),
        ),
        migrations.AddField(
            model_name='articlepost',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='Tags', to='article.articletag', verbose_name='برچسب ها'),
        ),
        migrations.CreateModel(
            name='ArticleCommentsLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.articlecomments', verbose_name='دیدگاه')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'لایک',
                'verbose_name_plural': 'لایک ها',
            },
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='article.articlepost', verbose_name='مقاله'),
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='article.articlecomments', verbose_name='والد'),
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]