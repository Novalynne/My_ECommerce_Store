from django.db import models
from _decimal import Decimal
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(max_length=280, blank=True)

    class Meta:
        db_table = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    description = models.TextField(max_length=280, blank=True)

    class Meta:
        db_table = "Sizes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, validators=[MinValueValidator(Decimal('0.01'))],decimal_places=2)
    categories = models.ManyToManyField(Category, blank=True)
    image = CloudinaryField('image', blank=True, null=True, default='placeholder')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, validators=[MinValueValidator(Decimal('0.01'))],decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.is_sale and self.price and self.sale_price:
            return round((self.price - self.sale_price) / self.price * 100)
        return 0



class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'Product_stock'
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.size.name} (Stock: {self.stock})"