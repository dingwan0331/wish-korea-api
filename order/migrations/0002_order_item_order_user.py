# Generated by Django 4.0.5 on 2022-06-21 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('auth', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ManyToManyField(through='order.OrderItem', to='product.item'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ManyToManyField(through='order.OrderItem', to='users.user'),
        ),
    ]
