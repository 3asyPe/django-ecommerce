from django.conf import settings

from typing import Union

from accounts.models import GuestEmail
from .models import BillingProfile, Card

import stripe


User = settings.AUTH_USER_MODEL


def load_billing_profile(request) -> Union[BillingProfile, None]:
    user = request.user
    guest_email = GuestEmail.objects.new_or_get(request)
    print(f"guest_email-{guest_email}")
    print(f"user-{user}")
    billing_profile = BillingProfile.objects.new_or_get(user=user, guest_email=guest_email)
    return billing_profile


def create_new_card(request) -> Union[Card, None]:
    if not request.POST:
        raise ValueError("request method is not POST")
    token = request.POST.get("token")
    if token is None:
        raise ValueError("request POST data doesn't contain token")
    billing_profile = load_billing_profile(request)
    if billing_profile is None:
        raise BillingProfile.DoesNotExist
    card_response = get_card_response(token=token, billing_profile=billing_profile)
    new_card = Card.objects.add_new(
        billing_profile=billing_profile, 
        stripe_card_response=card_response
    )
    return new_card

def get_card_response(token, billing_profile: BillingProfile):
    card_response = None
    if token is not None:
        card_response = stripe.Customer.create_source(
            id=billing_profile.customer_id,
            source=token,
        )
    return card_response
    

def has_associated_card(billing_profile: Union[BillingProfile, None]) -> bool:
    if billing_profile is not None:
        return billing_profile.has_card
    return False
