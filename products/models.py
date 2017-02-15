from django.db import models
from django.db.models.signals import post_save
from django.shortcuts import reverse
from django.utils.text import slugify


class ProductManager(models.Manager):
    def all(self):
        return self.get_queryset().filter(is_active=True)

    def get_related(self, instance):
        # all products in the same category
        related_all_products = self.get_queryset().filter(categories__in=instance.categories.all())

        # all products with the same default category
        related_default_products = self.get_queryset().filter(default_category=instance.default_category)

        # combine both lists and exclude the current product
        related_products = (related_all_products | related_default_products).exclude(id=instance.id).distinct()
        return related_products


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', blank=True)
    default_category = models.ForeignKey('Category', related_name='default_products', null=True, blank=True)
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.product.title, self.title)

    def get_price(self):
        if self.sale_price is not None and self.sale_price > 0:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


def product_post_save(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    # if the product has no variation , create a default one
    if variations.count() == 0:
        new_variation = Variation()
        new_variation.product = product
        new_variation.title = "Default"
        new_variation.price = product.price
        new_variation.save()

post_save.connect(product_post_save, sender=Product)


def image_upload_to(instance, filename):
    slug = slugify(instance.product.title)
    return 'products/{}/{}'.format(slug, filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return '{} - {}'.format(self.product.title, self.id)


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    descripton = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})
