from django.contrib import admin
from products.models import *


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price']
    inlines = [
        VariationInline,
        ProductImageInline
    ]

admin.site.register(Product, ProductAdmin)
# admin.site.register(Variation)
# admin.site.register(ProductImage)
admin.site.register(Category)
