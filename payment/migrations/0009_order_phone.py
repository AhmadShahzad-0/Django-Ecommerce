# Generated by Django 5.2.3 on 2025-07-03 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_alter_shippingaddress_shipping_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='0000000', max_length=15),
        ),
    ]
