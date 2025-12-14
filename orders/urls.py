from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("start/", views.start_payment, name="start_payment"),
    path("success/", views.payment_success, name="success"),
    path("cancel/", views.payment_cancel, name="cancel"),
]