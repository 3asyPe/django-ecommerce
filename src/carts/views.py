from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.services import (
    get_addresses_by_billing_profile,
    devide_addresses_on_shipping_and_billing,
)
from billing.models import BillingProfile
from billing.services import load_billing_profile
from orders.models import Order
from orders.services import load_order
from products.models import Product
from .models import Cart
from .services import (
    get_cart_and_update_session_data,
    update_cart_and_session_data,
    do_checkout,
)


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
        cart = update_cart_and_session_data(request, product_id=product_id)  
    return redirect("cart:home") 


def checkout_home(request):
    cart = get_cart_and_update_session_data(request)
    if cart.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    billing_profile = load_billing_profile(request)
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

    context = {
        "order": order,
        'billing_profile': billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "shipping_addresses": shipping_addresses,
        "billing_addresses": billing_addresses,
    }
    return render(request, 'carts/checkout.html', context)


def checkout_done(request):
    return render(request, 'carts/checkout-done.html', {})
