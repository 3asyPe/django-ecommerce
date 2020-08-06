from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart
from .services import (
    load_cart,
    update_cart,
    update_cart_part_of_session_data,
)


def cart_home(request):
    cart = load_cart(user=request.user)
    update_cart_part_of_session_data(request, cart=cart)
    context = {
        "cart": cart,
    }
    return render(request, "carts/home.html", context)


def cart_update(request):
    if request.POST:
        product_id = request.POST.get("product_id")
        cart = load_cart(user=request.user)
        update_cart(product_id=product_id, cart=cart)
        update_cart_part_of_session_data(request, cart=cart)   
    return redirect("cart:home") 
