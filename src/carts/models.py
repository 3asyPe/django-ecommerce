from django.conf import settings
from django.db import models
from django.db.models import QuerySet

from django.db.models.signals import pre_save, post_save, m2m_changed

from typing import Union

from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, user:User, cart_id: Union[int, None]=None):
        # No user no cart_id -> new cart
        # No user cart_id -> cart by cart_id or new cart
        # User no cart_id -> cart by user or new cart
        # User cart_id -> cart by cart_id or cart by user or new cart

        cart = None
        if not user.is_authenticated:
            cart_by_user_qs = self.get_queryset().none()
        else:
            cart_by_user_qs = self.get_queryset().filter(user=user, active=True)

        cart_by_id_qs = self.get_queryset().filter(id=cart_id, active=True)

        print("\n\n CartManager")
        print(f"cart_id-{cart_id}")
        print(f"user-{user}")
        print(f"cart_by_id_qs-{cart_by_id_qs}")
        print(f"cart_by_user_qs-{cart_by_user_qs}")

        print("\n\n Actions")
        if cart_by_id_qs.exists() and cart_by_user_qs.exists():
            cart_by_id = cart_by_id_qs.last()
            print("get cart_by_id")
            if cart_by_id_qs.last() != cart_by_user_qs.last():
                cart_by_user = cart_by_user_qs.last()
                print("get cart_by_user")
                if cart_by_id.products.all().count() == 0:
                    cart_by_id.delete()
                    print("delete cart_by_id")
                    cart = cart_by_user
                    print("cart_by_user is winner")
                else:
                    cart_by_user = cart_by_user_qs.last()
                    cart_by_user.delete()
                    print("delete cart_by_user")
                    cart = cart_by_id
                    print("cart_by_id is winner")
            else:
                cart = cart_by_id
                print("cart_by_id is winner")

        elif cart_by_user_qs.exists():
            cart = cart_by_user_qs.last()
            print("cart_by_user is winner")
        elif cart_by_id_qs.exists():
            cart_by_id = cart_by_id_qs.last()
            print('get cart_by_id')
            if user.is_authenticated and cart_by_id.user is None:
                cart_by_id.user = user
                print("set new user to cart_by_id")
                print(f"user{cart_by_id.user}")
                cart_by_id.save()
            cart = cart_by_id
            print("cart_by_id is winner")
        else:
            cart = self.new(user=user)
            print('created new cart')
        return cart

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
            print("m2m change")


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = float(instance.subtotal) * 0.99


pre_save.connect(pre_save_cart_receiver, sender=Cart)
