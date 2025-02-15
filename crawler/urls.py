from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("stock_list", views.stock_list, name="股票列表"),
    path("stock_by_id", views.stock_by_id, name="单股资讯"),
]