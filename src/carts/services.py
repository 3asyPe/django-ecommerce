from django.conf import settings

from typing import Union

from orders.models import Order
from products.models import Product
from .models import Cart


User = settings.AUTH_USER_MODEL


def get_cart_and_update_session_data(request) -> Cart:
    cart = _get_cart(request)
    update_cart_part_of_session_data(request, cart)
    return cart


def update_cart_and_session_data(request, product_id:int) -> Cart:
    cart = _get_cart(request)
    update_cart(product_id=product_id, cart=cart)
    update_cart_part_of_session_data(request, cart)
    return cart


def load_cart(user: User, cart_id: Union[int, None]) -> Cart:
    print("load_cart")
    cart = Cart.objects.new_or_get(user=user, cart_id=cart_id)
    return cart
    

def update_cart(product_id: int, cart: Cart) -> Cart:
    product = Product.objects.get(id=product_id)
    if product in cart.products.all():
        cart.products.remove(product)
    else:
        cart.products.add(product)
    print(cart.products.all())
    return cart


def update_cart_part_of_session_data(request, cart:Union[Cart, None]=None) -> None:
    if cart is None:
        cart_id = request.session.get("cart_id")
        cart = load_cart(user=request.user, cart_id=cart_id)
    request.session['cart_items_count'] = cart.products.count()
    request.session['cart_id'] = cart.id
    print(f"\n\nRequest session cart_id={request.session.get('cart_id')}")


def load_order(cart: Cart) -> Union[Order, None]:
    """Return order if cart is not empty else None"""
    if cart.products.count() == 0:
        return None
    
    order, order_created = Order.objects.get_or_create(cart=cart)
    return order


def _get_cart(request):
    cart_id = request.session.get("cart_id")
    user = request.user
    cart = load_cart(user=user, cart_id=cart_id)
    return cart
