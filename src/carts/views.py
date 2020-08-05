from django.shortcuts import render

from .models import Cart


def cart_home(request):
    cart_id = request.session.get("cart_id", None)
    cart_obj = Cart.objects.new_or_get(user=request.user, cart_id=cart_id)
    request.session['cart_id'] = cart_obj.id
    return render(request, "carts/home.html", {})\
