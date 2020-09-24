from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from accounts.services import get_next_path
from .models import BillingProfile
from .services import (
    load_billing_profile,
    create_new_card,
)

import stripe


STRIPE_SECRET_KEY = getattr(
    settings,
    "STRIPE_SECRET_KEY", 
    "sk_test_51HM8xIJWpkfHiKdZvgmZL84WTT571TOqAYHBN8xa9bp3kbv7XPKdjOJrfFFB4fJLx3SnUntrn5gAzQXaLuYjPY7g00n24pSpRM"
)
STRIPE_PUB_KEY = getattr(
    settings,
    "STRIPE_PUB_KEY",
    "pk_test_51HM8xIJWpkfHiKdZEUZVRXvZ2s7OP436CgUBwWquikW7fM73zwcwzEJkNcapaluBP6nEQ2LeHNMhGldmbpm405G300qiWFX2cN"
)
stripe.api_key = STRIPE_SECRET_KEY


def payment_method_view(request):
    billing_profile = load_billing_profile(request)
    if billing_profile is None:
        return redirect("/cart")
    nextUrl = get_next_path(request, "")
    context = {
        "publish_key": STRIPE_PUB_KEY,
        "next_url": nextUrl,
    }
    return render(request, "billing/payment-method.html", context)


def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        try:
            new_card = create_new_card(request)
        except BillingProfile.DoesNotExist:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        print(new_card)
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status_code=401)
