# Generated by Django 5.0.7 on 2024-07-18 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('gateways', '0003_alter_bank_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='نوع'),
        ),
    ]
