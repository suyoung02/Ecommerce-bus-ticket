# Generated by Django 4.0.5 on 2022-08-11 05:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0010_rename_first_name_payment_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
