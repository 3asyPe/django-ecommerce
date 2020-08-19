from django.conf import settings

from typing import Union

from accounts.models import GuestEmail
from .models import BillingProfile


User = settings.AUTH_USER_MODEL


def load_billing_profile(user: User, guest_email: GuestEmail) -> Union[BillingProfile, None]:
    billing_profile = None
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=user,
            email=user.email
        )
    elif guest_email is not None:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            email=guest_email.email
        )
    return billing_profile