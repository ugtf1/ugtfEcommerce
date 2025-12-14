import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(items, success_url, cancel_url):
    line_items = [{
        "price_data": {
            "currency": "usd",
            "product_data": {"name": i["product_name"]},
            "unit_amount": int(float(i["price"]) * 100),
        },
        "quantity": i["quantity"],
    } for i in items]
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )