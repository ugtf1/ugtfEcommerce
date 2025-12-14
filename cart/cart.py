from decimal import Decimal
from core.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, override=False):
        product = Product.objects.get(id=product_id)
        pid = str(product_id)
        if pid not in self.cart:
            self.cart[pid] = {"name": product.name, "price": str(product.price), "qty": 0, "thumbnail": product.thumbnail.url}
        self.cart[pid]["qty"] = quantity if override else self.cart[pid]["qty"] + quantity
        self.session.modified = True

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.session.modified = True

    def update(self, product_id, quantity):
        pid = str(product_id)
        if pid in self.cart:
            self.cart[pid]["qty"] = max(1, quantity)
            self.session.modified = True

    def __iter__(self):
        for pid, item in self.cart.items():
            item_price = Decimal(item["price"])
            item["subtotal"] = item_price * item["qty"]
            item["id"] = int(pid)
            yield item

    def total(self):
        return sum(Decimal(i["price"]) * i["qty"] for i in self.cart.values())

    def count(self):
        return sum(i["qty"] for i in self.cart.values())

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True