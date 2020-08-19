from django.conf import settings

from typing import Union

from carts.models import Cart
from billing.models import BillingProfile
from .models import Order


User = settings.AUTH_USER_MODEL



def load_order(billing_profile: BillingProfile, cart: Cart) -> Union[Order, None]:
    """Return order if cart and billing profile are not empty not empty else None"""
    print("load_order")
    if cart.products.count() == 0 or billing_profile is None:
        return None
    
    order = Order.objects.new_or_get(billing_profile=billing_profile, cart=cart)
    return order