from django.db import models
from accounts.models import Profile
from products.models import Product, Size
from _decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Create your models here.
class Order(models.Model):

    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="orders")
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    # TODO: add status field (e.g., pending, completed, cancelled), and shipping cost if applicable

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    def calculate_total(self): # calculate total price of the order
        return sum(item.line_total() for item in self.products.all())

    @staticmethod
    def place_order(user):
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return None  # no items in cart

        order = Order.objects.create(
            user=user,
            address=user.address,
            total=Decimal('0.00'),
        )

        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price
            )

        order.total = order.calculate_total()
        order.save()

        # clear the cart after placing the order
        cart_items.delete()

        return order



class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, validators=[MinValueValidator(Decimal('0.00'))], decimal_places=2) # price at the time of order

    class Meta:
        unique_together = ("order", "product")

    def line_total(self): # calculate total price for this product in the order
        return self.unit_price * self.quantity


class Cart(models.Model):

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="cart_user")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="cart_product")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='cart_product_size', default='M')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"Cart item {self.pk} for user {self.user}"

    @staticmethod
    def get_cart_for_user(user):
        return Cart.objects.filter(user=user)

    def user_cart_url(self):
        return reverse("cart", kwargs={"pk": self.pk}) #TODO: add urls.py

    # TODO: Add product to cart
    # TODO: Remove product from cart
    # TODO: Update quantity of product in cart