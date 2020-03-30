# Generated by Django 3.0.4 on 2020-03-30 07:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('set_app', '0010_auto_20200329_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(default=0, max_length=30, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only anumeric characters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(default='product code', max_length=30, unique=True),
        ),
    ]
