from django.db import models
from django.urls import reverse
from _decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def get_absolute_url(self):
        return reverse("product_category", kwargs={"pk": self.pk}) #TODO: add urls.py

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

    class Meta:
        db_table = 'products'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk}) #TODO: add urls.py

    def product_delete(self):
        return reverse("product_delete", kwargs={"pk": self.pk}) #TODO: add urls.py

    def product_modify(self):
        return reverse("product_modify", kwargs={"pk": self.pk}) #TODO: add urls.py


class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.size.name} (Stock: {self.stock})"