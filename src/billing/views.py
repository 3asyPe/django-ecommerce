from django.shortcuts import render
import stripe


stripe.api_key = "sk_test_51HM8xIJWpkfHiKdZvgmZL84WTT571TOqAYHBN8xa9bp3kbv7XPKdjOJrfFFB4fJLx3SnUntrn5gAzQXaLuYjPY7g00n24pSpRM"
STRIPE_PUB_KEY = "pk_test_51HM8xIJWpkfHiKdZEUZVRXvZ2s7OP436CgUBwWquikW7fM73zwcwzEJkNcapaluBP6nEQ2LeHNMhGldmbpm405G300qiWFX2cN"


def payment_method_view(request):
    if request.method == "POST":
        print(request.POST)
    context = {
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, "billing/payment-method.html", context)
