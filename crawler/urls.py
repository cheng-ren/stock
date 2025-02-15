from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("stock_by_id", views.stock_by_id, name="index"),
]