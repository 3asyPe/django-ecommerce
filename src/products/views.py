from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Product


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


def product_detail_view(request, pk:int):
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print("no product here")
    #     raise Http404("Product doesn't exitst")
    # except:
    #     print("huh?")

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("product doesn't exist")
    # print(instance)
    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exitst")

    context = {
        'object': instance
    }

    return render(request, "products/detail.html", context)


def product_featured_list_view(request):
    queryset = Product.objects.get_by_featured(True)
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


def product_featured_detail_view(request, pk:int):
    try:
        instance = Product.objects.get_by_featured(True).get(pk=pk)
    except Product.DoesNotExist:
        raise Http404("Product doesn't exist")
    print(instance)
    context = {
        'object': instance
    }
    return render(request, "products/featured-detail.html", context)
