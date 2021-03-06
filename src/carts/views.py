from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.services import (
    get_addresses_by_billing_profile,
    devide_addresses_on_shipping_and_billing,
)
from billing.models import BillingProfile
from billing.services import (
    load_billing_profile,
    has_associated_card,
)
from orders.models import Order
from orders.services import load_order
from products.models import Product
from .models import Cart
from .services import (
    get_cart_and_update_session_data,
    update_cart_and_session_data,
    do_checkout,
)

import stripe


STRIPE_SECRET_KEY = getattr(
    settings,
    "STRIPE_SECRET_KEY", 
    "sk_test_51HM8xIJWpkfHiKdZvgmZL84WTT571TOqAYHBN8xa9bp3kbv7XPKdjOJrfFFB4fJLx3SnUntrn5gAzQXaLuYjPY7g00n24pSpRM"
)
STRIPE_PUB_KEY = getattr(
    settings,
    "STRIPE_PUB_KEY",
    "pk_test_51HM8xIJWpkfHiKdZEUZVRXvZ2s7OP436CgUBwWquikW7fM73zwcwzEJkNcapaluBP6nEQ2LeHNMhGldmbpm405G300qiWFX2cN"
)
stripe.api_key = STRIPE_SECRET_KEY


def cart_detail_api_view(request):
    cart = get_cart_and_update_session_data(request)
    products = [{
        "id": p.id,
        "url": p.get_absolute_url(),
        "name": p.title,
        "price": p.price
        } for p in cart.products.all()
    ]
    cart_data = {
        "products": products,
        "subtotal": cart.subtotal,
        "total": cart.total,
    }
    return JsonResponse(cart_data)


def cart_home(request):
    cart = get_cart_and_update_session_data(request)
    print("\n\n cart_home")
    print(f"cart.id - {cart.id}")
    context = {
        "cart": cart,
    }
    return render(request, "carts/home.html", context)


def cart_update(request):
    if request.POST:
        product_id = request.POST.get("product_id")
        cart, product_added = update_cart_and_session_data(request, product_id=product_id)  
        if request.is_ajax():
            print("\n\nAJAX REQUEST\n\n")
            json_data = {
                "added": product_added,
                "removed": not product_added,
                "cartItemCount": cart.products.count(),
            }
            return JsonResponse(json_data)
    return redirect("cart:home") 


def checkout_home(request):
    cart = get_cart_and_update_session_data(request)
    if cart.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    billing_profile = load_billing_profile(request)
    has_card = has_associated_card(billing_profile=billing_profile)
    order = load_order(billing_profile=billing_profile, cart=cart)
    addresses = get_addresses_by_billing_profile(billing_profile=billing_profile)
    shipping_addresses, billing_addresses = devide_addresses_on_shipping_and_billing(
        addresses=addresses
    )

    print("checkout home")
    print(f"order-{order}")
    print(f"addresses-{addresses}")
    print(f"shipping_addresses-{shipping_addresses}")
    print(f"billing_addresses-{billing_addresses}")

    if request.method == "POST":
        success = do_checkout(request, order=order)
        if success:
            return redirect("cart:success")
        else:
            return redirect("card:checkout")

    context = {
        "order": order,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        'billing_profile': billing_profile,
        "shipping_addresses": shipping_addresses,
        "billing_addresses": billing_addresses,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, 'carts/checkout.html', context)


def checkout_done(request):
    return render(request, 'carts/checkout-done.html', {})
