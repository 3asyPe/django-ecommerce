from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Product


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


def product_detail_slug_view(request, slug:str):
    try:
        instance = Product.objects.get(slug=slug, active=True)
    except Product.DoesNotExist:
        raise Http404("Product doesn't exist")
    except Product.MultipleObjectsReturned:
        qs = Product.objects.filter(slug=slug, active=True)
        instance = qs.first()
    except:
        raise Http404("hmmm")
    print(instance)
    context = {
        'object': instance
    }
    return render(request, "products/featured-detail.html", context)
