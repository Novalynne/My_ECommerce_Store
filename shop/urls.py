from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartSummary.as_view(), name="cart_summary"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/", views.update_cart, name="update_cart"),
    path("wishlist/", views.wishlist.as_view(), name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("cart/checkout/payment/success", views.place_order, name="place_order"),
    path("order/<int:order_id>/cancel/", views.cancel_order, name="cancel_order"),
    path("order/", views.OrderSummery.as_view(), name="order_summary"),
    path("order/manage/", views.ManagerOrderList.as_view(), name="manage_orders"),
    path("order/manage/changestatus/<int:order_id>/", views.order_change_status, name="change_order_status"),
    path("order/<int:order_id>/return/", views.order_return, name="return_order"),
    path("order/<int:order_id>/return/confirm", views.submit_return_request, name="process_return"),
    path('order/<int:order_id>/returns/', views.return_requests_for_order, name='return_requests_for_order'),
]