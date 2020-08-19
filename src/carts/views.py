from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart
from .services import (
    get_cart_and_update_session_data,
    update_cart_and_session_data,
    load_order,
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

    billing_profile = None
    user = request.user
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get("guest_email_id")
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=user,
            email=user.email
        )
    elif guest_email_id is not None:
        try:
            guest_email = GuestEmail.objects.get(id=guest_email_id)
        except GuestEmail.DoesNotExist:
            request.session["guest_email_id"] = None
            raise GuestEmail.DoesNotExist
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            email=guest_email.email
        )

    order = load_order(billing_profile=billing_profile, cart=cart)

    print("checkout home")
    print(f"order-{order}")

    context = {
        "order": order,
        'billing_profile': billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }
    return render(request, 'carts/checkout.html', context)
