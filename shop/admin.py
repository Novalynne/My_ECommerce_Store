from django.contrib import admin
from .models import Order, OrderProduct, Cart, Status, ReturnRequest

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
admin.site.register(Status)
admin.site.register(ReturnRequest)