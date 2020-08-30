from django.shortcuts import render, get_object_or_404
from django.http import Http404

from analytics.services import send_object_viewed_data_to_analytics 
from carts.services import get_cart_and_update_session_data

from .models import Product
from .services import get_product_by_slug


def product_list_view(request):
    products = Product.objects.all()
    cart = get_cart_and_update_session_data(request)
    context = {
        'products_list': products,
        "cart": cart,
    }
    return render(request, "products/list.html", context)


def product_detail_slug_view(request, slug:str):
    product = get_product_by_slug(slug=slug)
    if product is None:
        raise Http404(f"Product with slug-{slug} doesn't exist")
    cart = get_cart_and_update_session_data(request)
    send_object_viewed_data_to_analytics(instance=product, request=request)
    context = {
        'object': product,
        'cart': cart,
    }
    return render(request, "products/detail.html", context)
