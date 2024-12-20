# Generated by Django 4.2.16 on 2024-11-10 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('text', models.TextField(verbose_name='متن پیام')),
                ('subject', models.CharField(default='Subject', max_length=255, verbose_name='عنوان')),
                ('is_read', models.BooleanField(default=False, verbose_name='خوانده شده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نوتیفیکیشن',
                'verbose_name_plural': 'نوتیفیکیشن ها',
            },
        ),
    ]
