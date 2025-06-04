from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=20, blank=True)
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    favorites = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def is_manager(self):
        return self.role == "manager"

    def is_client(self):
        return self.role == "client"
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


# TODO: add profile delete
# TODO: add profile register
# TODO: add profile login
# TODO: add profile add to favourites
# TODO: add profile details