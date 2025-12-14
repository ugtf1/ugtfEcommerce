from paypalcheckoutsdk.orders.orders_create_request import OrdersCreateRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from django.conf import settings

env = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
client = PayPalHttpClient(env)

def create_order(items, return_url, cancel_url):
    purchase_units = [{
        "amount": {
            "currency_code": "USD",
            "value": str(sum(float(i["price"]) * i["quantity"] for i in items)),
            "breakdown": {
                "item_total": {
                    "currency_code": "USD",
                    "value": str(sum(float(i["price"]) * i["quantity"] for i in items))
                }
            }
        },
        "items": [{
            "name": i["product_name"],
            "unit_amount": {"currency_code": "USD", "value": str(i["price"])},
            "quantity": i["quantity"],
        } for i in items]
    }]
    request = OrdersCreateRequest()
    request.prefer("return=representation")
    request.request_body({
        "intent": "CAPTURE",
        "purchase_units": purchase_units,
        "application_context": {"return_url": return_url, "cancel_url": cancel_url}
    })
    return client.execute(request)