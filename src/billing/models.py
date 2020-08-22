from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from accounts.models import GuestEmail


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

    objects = BillingManager()

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance: User, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
