from datetime import timezone, timedelta
from django.db import models
from accounts.models import Profile
from products.models import Product, Size
from _decimal import Decimal
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Statuses"

class Order(models.Model):

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    user_email = models.EmailField(max_length=254, default="unknown@example.com")
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="status")
    shipped_at = models.DateTimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    def update_status(self):
        if self.status.name == 'SHIPPED' and self.shipped_at:
            shipped_duration = timezone.now() - self.shipped_at
            if shipped_duration > timedelta(minutes=5):
                arrived_status = Status.objects.get(name='ARRIVED')
                self.status = arrived_status
                self.arrived_at = timezone.now()
                self.save()

    def non_refundable(self):
        if self.status.name == 'ARRIVED':
            refundable_time = timezone.now() - self.arrived_at
            if refundable_time > timedelta(minutes=5):
                non_refundable_status = Status.objects.get(name='NON REFUNDABLE')
                self.status = non_refundable_status
                self.save()


class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=255, default='Unknown Product')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default='M')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, validators=[MinValueValidator(Decimal('0.00'))], decimal_places=2) # price at the time of order

    class Meta:
        unique_together = ("order", "product", "size")

    def __str__(self):
        return f"Order {self.order.id} - {self.product_name} ({self.size})"



class Cart(models.Model):

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="cart_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_product")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='cart_product_size', default='M')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("user", "product", "size")

    def __str__(self):
        return f"Cart item {self.pk} for user {self.user}"

class ReturnRequest(models.Model):
    REASONS = [
        ('damaged', 'Damaged or defective'),
        ('wrong_item', 'Wrong item received'),
        ('not_satisfied', 'Not satisfied with the product'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="return_requests")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_products = models.ManyToManyField(OrderProduct)
    reason = models.CharField(max_length=20, choices=REASONS)
    notes = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        products = ', '.join([
            f"{op.product.name} ({op.size})"
            for op in self.order_products.all()
        ])
        return f"Return [{products}] from Order {self.order.id} by {self.user}"

