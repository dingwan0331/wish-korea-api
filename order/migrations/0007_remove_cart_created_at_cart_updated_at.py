# Generated by Django 4.0.5 on 2022-11-27 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_cart_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_at',
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
