from .cart import Cart
def cart_count(request):
    try:
        c = Cart(request)
        return {"cart_count": c.count()}
    except Exception:
        return {"cart_count": 0}