# Generated by Django 3.0.4 on 2020-03-19 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('set_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='mobile',
            field=models.CharField(default='123456901', max_length=11),
        ),
    ]
