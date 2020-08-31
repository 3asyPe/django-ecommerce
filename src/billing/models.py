from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from accounts.models import GuestEmail

import stripe

stripe.api_key = "sk_test_51HM8xIJWpkfHiKdZvgmZL84WTT571TOqAYHBN8xa9bp3kbv7XPKdjOJrfFFB4fJLx3SnUntrn5gAzQXaLuYjPY7g00n24pSpRM"

User = settings.AUTH_USER_MODEL


class BillingManager(models.Manager):
    def new_or_get(self, user: User, guest_email: GuestEmail):
        billing_profile = None
        if user.is_authenticated:
            billing_profile, billing_profile_created = self.get_or_create(
                user=user,
                email=user.email
            )
        elif guest_email is not None:
            billing_profile, billing_profile_created = self.get_or_create(
                email=guest_email.email
            )
        return billing_profile


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingManager()

    def __str__(self):
        return self.email


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to stripe")
        customer = stripe.Customer.create(
            email=instance.email
        )
        print(customer)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance: User, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
