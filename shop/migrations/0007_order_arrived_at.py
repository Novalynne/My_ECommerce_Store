# Generated by Django 5.2 on 2025-06-27 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0006_order_shipped_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="arrived_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
