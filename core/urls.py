from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path("products/", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path("search/", views.search, name="search"),
]