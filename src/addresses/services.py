from django.db.models import QuerySet
from django.forms.models import model_to_dict

from typing import Union

from billing.models import BillingProfile
from billing.services import load_billing_profile
from orders.services import add_address_to_order
from .models import Address


def finalize_the_address(request, instance: Address, address_type="shipping") -> (Address, bool):
    """Loads billing profile and if it exists adds to existing address object
    with all required fields. After adding update an instance in db.
    Then associate address to order"""
    billing_profile = load_billing_profile(request)
    print("\n\n finalize the address")
    if billing_profile is not None:
        instance.billing_profile = billing_profile
        instance.address_type = address_type
        instance = get_or_create_address(instance)
        add_address_to_order(request, address=instance)
        set_shipping_address_as_active(
            request,
            shipping_address_id=instance.id,
            address_type=instance.address_type
        )
        print(f"\n\naddress saved-{instance}")
        return instance, True
    print("instance not saved")
    return instance, False


def get_addresses_by_billing_profile(billing_profile: BillingProfile) -> Union[QuerySet, None]:
    if billing_profile is not None:
        addresses = Address.objects.filter(billing_profile=billing_profile)
        return addresses
    return None


def get_address_by_id(address_id: int) -> Union[Address, None]:
    print("\n\n get_address_by_id")
    print(f"address_id-{address_id}")
    if address_id is not None:
        address = Address.objects.get(id=address_id)
        print(f"address-{address}")
        return address
    return None


def get_or_create_address(address: Address) -> Address:
    address, address_created = Address.objects.get_or_create(
        billing_profile=address.billing_profile,
        address_type=address.address_type,
        address_line_1=address.address_line_1,
        address_line_2=address.address_line_2,
        city=address.city,
        country=address.country,
        state=address.state,
        postal_code=address.postal_code
    )
    print(f"ADDRESS-{address}")
    return address


def set_shipping_address_as_active(request, shipping_address_id: int, address_type: str):
    if shipping_address_id is not None:
        qs = Address.objects.filter(id=shipping_address_id)
        if qs.exists():
            request.session[f"active_{address_type}_address_id"] = address.id
