from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile.as_view(), name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/edit/delete/', views.delete_profile_view, name='delete_profile'),
]