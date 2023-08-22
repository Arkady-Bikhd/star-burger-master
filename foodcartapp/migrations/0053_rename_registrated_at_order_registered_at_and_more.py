# Generated by Django 4.2.3 on 2023-08-22 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='registrated_at',
            new_name='registered_at',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Э', 'Электронно'), ('Н', 'Наличностью')], db_index=True, max_length=2, null=True, verbose_name='Способ оплаты'),
        ),
    ]
