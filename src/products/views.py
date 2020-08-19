from django.shortcuts import render, get_object_or_404
from django.http import Http404

from carts.services import get_cart_and_update_session_data

from .models import Product
from .services import get_product_by_slug


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


def product_detail_slug_view(request, slug:str):
    product = get_product_by_slug(slug=slug)
    cart = get_cart_and_update_session_data(request)
    context = {
        'object': product,
        'cart': cart,
    }
    return render(request, "products/detail.html", context)
