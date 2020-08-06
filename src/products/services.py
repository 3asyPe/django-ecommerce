from django.http import Http404

from .models import Product


def get_product_by_slug(slug) -> Product:
    try:
        instance = Product.objects.get(slug=slug, active=True)
    except Product.DoesNotExist:
        raise Http404("Product doesn't exist")
    except Product.MultipleObjectsReturned:
        qs = Product.objects.filter(slug=slug, active=True)
        instance = qs.first()
    except:
        raise Http404("hmmm")
    return instance
