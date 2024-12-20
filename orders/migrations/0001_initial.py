# Generated by Django 4.2.16 on 2024-11-10 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gateways.utils
import phonenumber_field.modelfields
import products.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('area', '0001_initial'),
        ('account', '0001_initial'),
        ('coupon', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('tracking_code', models.CharField(editable=False, max_length=255, verbose_name='شماره پیگیری سفارش')),
                ('through', models.CharField(max_length=50, verbose_name='از طریق')),
                ('first_name', models.CharField(max_length=200, verbose_name='نام')),
                ('last_name', models.CharField(max_length=200, verbose_name='نام خانوادگی')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=50, region=None, verbose_name='شماره موبایل')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('province', models.CharField(max_length=200, verbose_name='استان')),
                ('city', models.CharField(max_length=200, verbose_name='شهر')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='کد پستی')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('commodity_prices', models.CharField(blank=True, max_length=20, null=True, verbose_name='قیمت کالاها')),
                ('total_discount', models.CharField(blank=True, max_length=20, null=True, verbose_name='تخفیف')),
                ('discount_amount', models.CharField(blank=True, max_length=20, null=True, verbose_name='مبلغ کوپن تخفیف')),
                ('payable', models.CharField(blank=True, max_length=20, null=True, verbose_name='قابل پرداخت')),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True, verbose_name='روش پرداخت')),
                ('order_created', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ ایجاد سفارش')),
            ],
            options={
                'verbose_name': 'صورت حساب',
                'verbose_name_plural': 'صورت حساب ها',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('tracking_code', models.CharField(default=gateways.utils.generate_tracking_code, editable=False, max_length=255, unique=True, verbose_name='شماره پیگیری')),
                ('reference_code', models.CharField(default=gateways.utils.generate_reference_code, editable=False, max_length=255, unique=True, verbose_name='کد ارجاع')),
                ('postal_tracking_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='کد رهگیری پستی')),
                ('through', models.PositiveSmallIntegerField(choices=[(1, 'سایت'), (2, 'شبکه های اجتماعی'), (3, 'فروشگاه')], default=1, verbose_name='از طریق')),
                ('order_status', models.PositiveSmallIntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'در انتظار بررسی'), (3, 'در حال انجام'), (4, 'بسته بندی'), (6, 'ارسال شده'), (5, 'تکمیل شده'), (8, 'لغو شده'), (9, 'مسترد شده')], default=1, verbose_name='وضعیت سفارش')),
                ('send_notification_sms', models.BooleanField(default=True, verbose_name='ارسال پیامک اطلاع رسانی')),
                ('mark_order', models.BooleanField(default=False, help_text='سفارش را برای موارد خاص مثل تاخیر در بسته بندی، مشکل در پرداخت یا... علامت گذاری کنید.', verbose_name='نشان کردن')),
                ('first_name', models.CharField(max_length=200, verbose_name='نام')),
                ('last_name', models.CharField(max_length=200, verbose_name='نام خانوادگی')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=50, region=None, verbose_name='شماره موبایل')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('province', models.CharField(max_length=200, verbose_name='استان')),
                ('city', models.CharField(max_length=200, verbose_name='شهر')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='کد پستی')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('commodity_prices', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قیمت کالاها')),
                ('total_discount', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='تخفیف')),
                ('discount_amount', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='مبلغ کوپن تخفیف')),
                ('prepayment', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='بیعانه')),
                ('payable', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قابل پرداخت')),
                ('payment_method', models.PositiveSmallIntegerField(choices=[(1, 'درگاه بانکی'), (2, 'کیف پول'), (3, 'کارت به کارت'), (4, 'پرداخت در محل'), (5, 'دستگاه پوز'), (6, 'نقدی')], default=1, verbose_name='روش پرداخت')),
                ('paid', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('deposit_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ واریز')),
                ('user_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
                ('user_agent', models.JSONField(blank=True, null=True, verbose_name='User Agent')),
                ('register_in_accounting_system', models.BooleanField(default=False, verbose_name='ثبت در سیستم حسابداری')),
                ('address_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.useraddress', verbose_name='آدرس')),
                ('city_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='area.city', verbose_name='شهر')),
                ('discount_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupon.discountcoupon', verbose_name='کوپن تخفیف')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارشات',
                'ordering': ('-created',),
            },
            bases=(products.mixins.ModelDiffMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PackingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
            ],
            options={
                'verbose_name': 'نوع بسته بندی',
                'verbose_name_plural': 'انواع بسته بندی',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام')),
                ('price', models.PositiveBigIntegerField(blank=True, verbose_name='قیمت')),
                ('discount', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='تخفیف')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')),
                ('total_price', models.PositiveBigIntegerField(blank=True, verbose_name='جمع کالاها')),
                ('total_discount', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='جمع تخفیف')),
                ('amount_payable', models.PositiveBigIntegerField(blank=True, verbose_name='قابل پرداخت')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='سفارش')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product', verbose_name='محصول')),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category', verbose_name='دسته بندی')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variant', verbose_name='تنوع محصول')),
            ],
            options={
                'verbose_name': 'آیتم سفارش',
                'verbose_name_plural': 'آیتم های سفارش',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='packing_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.packingtype', verbose_name='بسته بندی'),
        ),
        migrations.AddField(
            model_name='order',
            name='province_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='area.province', verbose_name='استان'),
        ),
        migrations.AddField(
            model_name='order',
            name='registrar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrar_set', to=settings.AUTH_USER_MODEL, verbose_name='فروشنده'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='مشتری'),
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('variant_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='شناسه')),
                ('product', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام محصول')),
                ('sku', models.CharField(blank=True, max_length=255, null=True, verbose_name='شناسه SKU')),
                ('price', models.PositiveBigIntegerField(blank=True, verbose_name='قیمت')),
                ('discount', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='تخفیف')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='تعداد')),
                ('total_price', models.PositiveBigIntegerField(blank=True, verbose_name='جمع کالاها')),
                ('total_discount', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='جمع تخفیف')),
                ('amount_payable', models.PositiveBigIntegerField(blank=True, verbose_name='قابل پرداخت')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.invoice', verbose_name='صورت حساب')),
            ],
            options={
                'verbose_name': 'آیتم صورت حساب',
                'verbose_name_plural': 'آیتم های صورت حساب',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order', verbose_name='سفارش'),
        ),
    ]
