from django.urls import path

from . import views

urlpatterns = [
    path("tool", views.index, name="index"),
    path("automatic_first", views.automatic_first_of_day, name="自动化爬虫"),
    path("automatic_every", views.automatic_every_hour_of_day, name="自动化爬虫"),
    path("stock_list", views.stock_list, name="股票列表"),
    path("stock_by_id", views.stock_by_id, name="单股资讯"),
]