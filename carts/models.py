from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.shortcuts import reverse

from products.models import Variation


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Variation, through='CartItem')
    subtotal = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    total_tax = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        self.subtotal = 0
        for item in self.cartitem_set.all():
            self.subtotal += item.line_total
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(decimal_places=2, max_digits=20)

    def __str__(self):
        return self.item.title

    def remove(self):
        return '{}?item={}&del=True'.format(reverse('cart'), self.item.id)


def pre_save_cart_item(sender, instance, *args, **kwargs):
    qty = Decimal(instance.quantity)
    if qty >= 1:
        price = instance.item.get_price()
        instance.line_total = qty * price


def post_save_cart_item(sender, instance,  *args, **kwargs):
    instance.cart.update_subtotal()

pre_save.connect(pre_save_cart_item, sender=CartItem)
post_save.connect(post_save_cart_item, sender=CartItem)
post_delete.connect(post_save_cart_item, sender=CartItem)


# tax and totatl price calculations for each cart
def calculate_total_price(sender, instance, *args, **kwargs):
    tax_percentage = settings.TAX_PERCENTAGE
    total_tax = instance.subtotal * Decimal(tax_percentage)
    total_price = instance.subtotal + total_tax

    instance.total_tax = round(total_tax, 2)
    instance.total_price = round(total_price, 2)

pre_save.connect(calculate_total_price, sender=Cart)
