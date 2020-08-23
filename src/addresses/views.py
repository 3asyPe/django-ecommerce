from django.shortcuts import render, redirect

from accounts.services import get_next_path
from orders.services import add_address_to_order
from .services import finalize_the_address, get_address_by_id
from .forms import AddressForm


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        print(request.POST)
        address = form.save(commit=False)
        address_type = request.POST.get("address_type", 'shipping')
        address, address_created = finalize_the_address(request, instance=address, address_type=address_type)
        
        if not address_created:
            print("ERROR HERE")
            return redirect("/cart:checkout/")
        
        path = get_next_path(request, base_url='/cart:checkout/')
        return redirect(path)

    return redirect("/cart:checkout/")


def checkout_address_reuse_view(request):
    context = {}

    if request.method == "POST":
        print(request.POST)
        shipping_address_id = request.POST.get("address", None)
        address = get_address_by_id(shipping_address_id)
        add_address_to_order(request, address=address)
        path = get_next_path(request, base_url='/cart:checkout/')
        return redirect(path)

    return redirect("/cart:checkout/")
