from django.contrib import admin
from .models import Order, OrderProduct, Cart

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)