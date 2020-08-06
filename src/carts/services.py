from django.conf import settings

from products.models import Product
from .models import Cart


User = settings.AUTH_USER_MODEL


def load_cart(user: User) -> Cart:
    cart = Cart.objects.new_or_get(user=user)
    return cart
    

def update_cart(product_id: int, cart: Cart) -> Cart:
    product = Product.objects.get(id=product_id)
    if product in cart.products.all():
        cart.products.remove(product)
    else:
        cart.products.add(product)
    return cart


def update_cart_part_of_session_data(request, cart: Cart) -> None:
    request.session['cart_items_count'] = cart.products.count()
