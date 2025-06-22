from django.contrib import admin
from .models import Order, OrderProduct, Cart, Status

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
admin.site.register(Status)