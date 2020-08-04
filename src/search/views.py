from django.shortcuts import render

from products.models import Product


def search_product_list_view(request):
    query = request.GET.get("q")
    if query is not None:
        queryset = Product.objects.filter(title__icontains=query)
    else:
        queryset = Product.objects.get_by_featured()
    context = {
        'object_list': queryset
    }
    return render(request, "search/view.html", context)
