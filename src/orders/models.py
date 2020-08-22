from django.db import models
from django.db.models.signals import pre_save, post_save

from math import fsum

from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile: BillingProfile, cart: Cart):
        print("\n\n order manager")
        try:
            order = self.get(cart=cart)
        except Order.DoesNotExist:
            order = None
        print(f"billing_profile-{billing_profile}")
        print(f"cart-{cart}")
        print(f"order-{order}")

        print("\n\n actions")
        if order is None:
            order = self.create(billing_profile=billing_profile, cart=cart)
            print(f"created new order-{order}")
        elif order.billing_profile != billing_profile:
            shipping_address = order.shipping_address
            billing_address = order.billing_address
            order.delete()
            new_order = self.create(billing_profile=billing_profile, cart=cart)
            new_order.shipping_address = shipping_address
            new_order.billing_address = billing_address
            print(f"order-{order}")
            print("deleted previous order")
            order = new_order
            print(f"created new order-{order}")
        return order


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", on_delete=models.CASCADE, null=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name="billing_address", on_delete=models.CASCADE, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = fsum([cart_total, shipping_total])
        formated_total = format(new_total, ".2f")
        self.total = formated_total
        self.save()
        return new_total


def pre_save_create_order_id(sender, instance: Order, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance: Cart, created, *args, **kwargs):
    if not created and hasattr(instance, 'order'):
        cart_obj = instance
        cart_total = cart_obj.total
        order_obj = cart_obj.order
        order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance: Order, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
