from django.db import models


class GuestEmailManager(models.Manager):
    def new_or_get(self, request, email=None):
        email = request.session.get("guest_email") if email is None else email
        print("get_guest_email")
        if email is None:
            return None
        guest_email, guest_email_created = self.get_or_create(email=email)
        request.session["guest_email"] = guest_email.email
        return guest_email



class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = GuestEmailManager()

    def __str__(self):
        return self.email
