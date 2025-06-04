from django.db import models
from accounts.models import Profile
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]   # 1–5
    )
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")  # one review per user per product
        ordering = ["-date"]

    def __str__(self):
        return f"Review {self.rating}/5 by {self.user} on {self.product}"

    # TODO: add review
    # TODO: add review update
    # TODO: add review delete