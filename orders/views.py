from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cart.cart import Cart
from .models import Order, OrderItem
from .services.stripe_gateway import create_checkout_session
from .services.paypal_gateway import create_order

@login_required
def checkout(request):
    cart = Cart(request)
    items = []
    for i in cart:
        items.append({
            "product_name": i["name"],
            "price": i["price"],
            "quantity": i["qty"],
            "thumbnail": i["thumbnail"],
        })
    return render(request, "orders/checkout.html", {"cart": cart, "items": items, "total": cart.total()})

@login_required
def start_payment(request):
    method = request.POST.get("method")  # "stripe" or "paypal"
    cart = Cart(request)
    items = [{"product_name": i["name"], "price": i["price"], "quantity": i["qty"]} for i in cart]
    success_url = request.build_absolute_uri(reverse("orders:success"))
    cancel_url = request.build_absolute_uri(reverse("orders:cancel"))

    if method == "stripe":
        session = create_checkout_session(items, success_url, cancel_url)
        return redirect(session.url)
    else:
        pp_order = create_order(items, success_url, cancel_url)
        for link in pp_order.result.links:
            if link.rel == "approve":
                return redirect(link.href)
    return redirect("orders:checkout")

@login_required
def payment_success(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user, total=cart.total(), status="paid")
    for i in cart:
        OrderItem.objects.create(
            order=order,
            product_name=i["name"],
            price=i["price"],
            quantity=i["qty"],
            thumbnail=i["thumbnail"],
        )
    cart.clear()
    return render(request, "orders/success.html", {"order": order})

@login_required
def payment_cancel(request):
    return render(request, "orders/cancel.html")