# Generated by Django 4.2.3 on 2023-07-22 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product_amount',
            new_name='quantity',
        ),
    ]
