from django.urls import path
from . import views


urlpatterns = [
    path('product/<int:pk>', views.product, name='product'),
    path('category/manage/', views.manage_categories, name='manage_categories'),
    path('add/', views.add_to_shop, name='add_to_shop'),
    path('edit/<int:pk>', views.edit_product, name='edit_product'),
    path('edit/<int:pk>/delete/', views.delete_product, name='delete_product'),
]