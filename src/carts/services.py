from django.conf import settings

from typing import Union

from orders.models import Order
from orders.services import check_order_done, mark_order_as_paid
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


def delete_cart_part_of_session_data(request):
    del request.session['cart_items_count']
    del request.session['cart_id']


def do_checkout(request, order: Order) -> bool:
    order_is_done = check_order_done(order)
    if order_is_done:
        mark_order_as_paid(order)
        cart = order.cart
        _unactivate_cart(cart=cart)
        delete_cart_part_of_session_data(request)
        return True
    return False


def _unactivate_cart(cart: Cart):
    cart.active = False
    cart.save()


def _get_cart(request):
    cart_id = request.session.get("cart_id")
    user = request.user
    cart = load_cart(user=user, cart_id=cart_id)
    return cart
