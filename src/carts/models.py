from django.conf import settings
from django.db import models

from django.db.models.signals import pre_save, post_save, m2m_changed

from typing import Union

from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, user:User):
        qs = self.get_queryset().filter(user=user, active=True)
        if qs.exists():
            cart_obj = qs.last()
            if user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=user)
        return cart_obj

    def new(self, user=None):
        user_obj = user if user is not None and user.is_authenticated else None
        return self.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if "post_" in action:
        products = instance.products.all()
        total = 0
        for p in products:
            total += p.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = float(instance.subtotal) * 0.99


pre_save.connect(pre_save_cart_receiver, sender=Cart)
