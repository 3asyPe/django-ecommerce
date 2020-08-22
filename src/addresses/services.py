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
        instance.save()
        add_address_to_order(request, address=instance)
        print(f"instance save-{instance}")
        return instance, True
    print("instance not saved")
    return instance, False
