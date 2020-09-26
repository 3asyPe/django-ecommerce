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


def update_cart_and_session_data(request, product_id:int) -> (Cart, bool):
    cart = _get_cart(request)
    cart, product_added = update_cart(product_id=product_id, cart=cart)
    update_cart_part_of_session_data(request, cart)
    return cart, product_added


def load_cart(user: User, cart_id: Union[int, None]) -> Cart:
    print("load_cart")
    cart = Cart.objects.new_or_get(user=user, cart_id=cart_id)
    return cart
    

def update_cart(product_id: int, cart: Cart) -> (Cart, bool):
    product = Product.objects.get(id=product_id)
    if product in cart.products.all():
        cart.products.remove(product)
        return cart, False
    else:
        cart.products.add(product)
        return cart, True


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
        billing_profile = order.billing_profile
        charged, charge_msg = billing_profile.charge(order)
        if charged:
            mark_order_as_paid(order)
            cart = order.cart
            _deactivate_cart(cart=cart)
            delete_cart_part_of_session_data(request)
            if not billing_profile.user:
                billing_profile.set_cards_inactive()
            return True
        else:
            print(charge_msg)
    return False


def _deactivate_cart(cart: Cart):
    cart.active = False
    cart.save()


def _get_cart(request):
    cart_id = request.session.get("cart_id")
    user = request.user
    cart = load_cart(user=user, cart_id=cart_id)
    return cart
