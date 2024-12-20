# Generated by Django 4.2.16 on 2024-11-10 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetadataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='شی مرتبط')),
                ('field', models.CharField(max_length=255, verbose_name='فیلد')),
                ('value', models.TextField(verbose_name='مقدار')),
                ('value_fa', models.TextField(null=True, verbose_name='مقدار')),
                ('value_en', models.TextField(null=True, verbose_name='مقدار')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='نوع محتوا')),
            ],
            options={
                'verbose_name': 'تگ متا',
                'verbose_name_plural': 'تگ های متا',
            },
        ),
    ]
