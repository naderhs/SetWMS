# Generated by Django 3.0.4 on 2020-04-18 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('set_app', '0005_auto_20200413_1847'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transaction',
            new_name='OrderItem',
        ),
    ]
