# Generated by Django 4.2.3 on 2023-08-01 10:53

from django.db import migrations


def fill_order_item_price(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for order_item in OrderItem.objects.all().iterator():
        order_item.price = order_item.product.price
        order_item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_alter_orderitem_managers_orderitem_price'),
    ]

    operations = [
        migrations.RunPython(fill_order_item_price)
    ]
