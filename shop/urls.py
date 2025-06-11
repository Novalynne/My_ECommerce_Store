from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_summary.as_view(), name="cart_summary"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/", views.update_cart, name="update_cart"),
    path("wishlist/", views.wishlist.as_view(), name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
]