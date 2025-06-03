from django.urls import path
from . import views
from .views import Login

urlpatterns = [
    path("", Login, name="login"),
]