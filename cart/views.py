from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from core.models import Product
from .cart import Cart

def cart_view(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart, "total": cart.total()})

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id, quantity=1)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"count": cart.count(), "total": str(cart.total())})
    return redirect("cart:cart_view")

def update_cart(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get("qty", 1))
    cart.update(product_id, qty)
    return JsonResponse({"count": cart.count(), "total": str(cart.total())})

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse({"count": cart.count(), "total": str(cart.total())})