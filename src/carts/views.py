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
    order = None
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

    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart, active=True)
        if order_qs.count() == 1:
            order = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(billing_profile=billing_profile) \
                                        .filter(cart=cart, active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order = Order.objects.create(billing_profile=billing_profile, cart=cart)

    context = {
        "order": order,
        'billing_profile': billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }
    return render(request, 'carts/checkout.html', context)
