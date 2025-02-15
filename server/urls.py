from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("query_news", views.query_news, name="index"),
    path("query_stock", views.query_stock, name="index"),
]