from django.urls import path
from . import views


urlpatterns = [
    path("", views.frontpage, name="frontpage"),
    path("homepage/", views.homepage.as_view(), name="homepage"),
    #path('homepage/search/', views.search_page_view(), name='search'),
]