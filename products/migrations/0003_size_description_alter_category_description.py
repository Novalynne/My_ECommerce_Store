# Generated by Django 5.2.1 on 2025-06-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_size_product_stock_alter_product_image_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='description',
            field=models.TextField(blank=True, max_length=280),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, max_length=280),
        ),
    ]
