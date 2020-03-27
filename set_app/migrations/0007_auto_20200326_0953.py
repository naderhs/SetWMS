# Generated by Django 3.0.4 on 2020-03-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('set_app', '0006_customer_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='type',
        ),
        migrations.AddField(
            model_name='customer',
            name='entity_type',
            field=models.CharField(choices=[('IN', 'Freshman'), ('CO', 'Sophomore'), ('OT', 'Junior')], default='IN', max_length=2),
        ),
    ]