from django.urls import path
from . import views


urlpatterns = [
    path('product/<int:pk>', views.product, name='product'),
]