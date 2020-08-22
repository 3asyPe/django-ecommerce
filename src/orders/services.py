from django.conf import settings

from typing import Union

from addresses.models import Address
from billing.models import BillingProfile
from billing.services import load_billing_profile
from carts.models import Cart
from carts.services import get_cart_and_update_session_data
from .models import Order


User = settings.AUTH_USER_MODEL



def load_order(billing_profile: BillingProfile, cart: Cart) -> Union[Order, None]:
    """Return order if cart and billing profile are not empty not empty else None"""
    print("load_order")
    if cart.products.count() == 0 or billing_profile is None:
        return None
    
    order = Order.objects.new_or_get(billing_profile=billing_profile, cart=cart)
    return order


def add_address_to_order(request, address:Address, order: Order=None):
    print("\n\n add address to order")
    print(f"address-{address}")
    if order is None:
        billing_profile = load_billing_profile(request)
        cart = get_cart_and_update_session_data(request)
        order = load_order(billing_profile=billing_profile, cart=cart)
    print(f'order-{order}')
    if address.address_type == "shipping":
        order.shipping_address = address
    elif address.address_type == "billing":
        order.billing_address = address
    else:
        raise RuntimeError("This type of address is not handled or address is None")
    order.save()
