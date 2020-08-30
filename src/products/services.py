from django.http import Http404

from typing import Union

from .models import Product


def get_product_by_slug(slug) -> Union[Product, None]:
    try:
        instance = Product.objects.get(slug=slug, active=True)
    except Product.DoesNotExist:
        instance = None
    except Product.MultipleObjectsReturned:
        qs = Product.objects.filter(slug=slug, active=True)
        instance = qs.first()
    return instance
