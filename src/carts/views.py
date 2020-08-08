from django.shortcuts import render, redirect

from orders.models import Order
from products.models import Product
from .models import Cart
from .services import (
    load_cart,
    load_order,
    update_cart,
    update_cart_part_of_session_data,
)


def cart_home(request):
    cart = load_cart(user=request.user)
    update_cart_part_of_session_data(request)
    context = {
        "cart": cart,
    }
    return render(request, "carts/home.html", context)


def cart_update(request):
    if request.POST:
        product_id = request.POST.get("product_id")
        cart = load_cart(user=request.user)
        update_cart(product_id=product_id, cart=cart)
        update_cart_part_of_session_data(request)   
    return redirect("cart:home") 


def checkout_home(request):
    cart = load_cart(user=request.user)
    order = load_order(cart=cart)
    if order is None:
        return redirect("cart:home")
    context = {
        "order": order
    }
    print(order)
    return render(request, 'carts/checkout.html', context)
