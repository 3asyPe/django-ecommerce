from django.shortcuts import render, redirect

from accounts.services import get_next_path
from .services import finalize_the_address
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
