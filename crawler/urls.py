from django.urls import path

from . import views

urlpatterns = [
    path("tool", views.index, name="index"),
    path("automatic", views.automatic, name="自动化爬虫"),
    path("stock_list", views.stock_list, name="股票列表"),
    path("stock_by_id", views.stock_by_id, name="单股资讯"),
]