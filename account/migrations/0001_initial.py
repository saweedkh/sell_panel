# Generated by Django 4.2.16 on 2024-11-10 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='نام کاربری')),
                ('full_name', models.CharField(max_length=255, verbose_name='نام و نام خانوادگی')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=50, null=True, region=None, unique=True, verbose_name='شماره موبایل')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='users/avatar/%y/%m/%d', verbose_name='تصویر پروفایل')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='ادمین')),
                ('is_staff', models.BooleanField(default=False, verbose_name='کارمند')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('confirm_profile', models.BooleanField(default=False, verbose_name='تایید پروفایل')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='MobilePhoneVerify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='شماره موبایل')),
                ('code', models.IntegerField(blank=True, null=True, verbose_name='کد')),
                ('status', models.IntegerField(choices=[(0, 'قابل استفاده'), (1, 'غیر قابل استفاده')], default=0, verbose_name='وضعیت')),
            ],
            options={
                'verbose_name': 'کد تایید',
                'verbose_name_plural': 'کد های تایید',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام محل')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=255, null=True, region=None, verbose_name='شماره تلفن')),
                ('postal_code', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='کدپستی')),
                ('is_default', models.BooleanField(default=False, verbose_name='پیشفرض برای این ادرس ارسال شود')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
                'ordering': ('-created',),
            },
        ),
    ]
