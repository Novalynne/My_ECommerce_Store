# Generated by Django 5.2 on 2025-06-28 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0011_alter_returnrequest_order_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="returnrequest",
            name="order_product",
        ),
        migrations.AddField(
            model_name="returnrequest",
            name="order_products",
            field=models.ManyToManyField(to="shop.orderproduct"),
        ),
    ]
