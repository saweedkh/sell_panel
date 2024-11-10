# Generated by Django 4.2.16 on 2024-11-10 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='نام')),
                ('name_fa', models.CharField(max_length=255, null=True, unique=True, verbose_name='نام')),
                ('name_en', models.CharField(max_length=255, null=True, unique=True, verbose_name='نام')),
            ],
            options={
                'verbose_name': 'استان',
                'verbose_name_plural': 'استان ها',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('name_fa', models.CharField(max_length=255, null=True, verbose_name='نام')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='نام')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='area.province', verbose_name='استان')),
            ],
            options={
                'verbose_name': 'شهر',
                'verbose_name_plural': 'شهر ها',
                'unique_together': {('province', 'name')},
            },
        ),
    ]
