from django.conf import settings

from typing import Union

from accounts.services import get_or_create_guest_email
from .models import BillingProfile


User = settings.AUTH_USER_MODEL


def load_billing_profile(request) -> Union[BillingProfile, None]:
    user = request.user
    guest_email = get_or_create_guest_email(request)
    print(f"guest_email-{guest_email}")
    print(f"user-{user}")
    billing_profile = BillingProfile.objects.new_or_get(user=user, guest_email=guest_email)
    return billing_profile