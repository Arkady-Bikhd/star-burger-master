# Generated by Django 4.2.3 on 2023-08-04 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='foodcartapp.restaurant', verbose_name='Ресторан'),
        ),
    ]
