from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from products.models import Product, Variation, Category
from products.forms import VariationInventoryFormSet

from products.mixins import StaffRequiredMixin


class VariationListView(StaffRequiredMixin, ListView):
    model = Variation
    context_object_name = 'variation_list'
    template_name = 'products/variation_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            qs = Variation.objects.filter(product=product)
        return qs

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_variation = form.save(commit=False)
                if new_variation.title:
                    product_pk = self.kwargs.get('pk')
                    product = get_object_or_404(Product, pk=product_pk)
                    new_variation.product = product
                    new_variation.save()

        messages.success(request, 'Inventory and prices updated')
        return redirect(reverse('product_list'))


class ProductListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'products/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, *kwargs)
        query = self.request.GET.get('search')
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains = query) |
                Q(description__icontains=query)
            )
        return qs


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['related'] = Product.objects.get_related(self.get_object())[:5]
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'category_list'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        category = self.get_object()
        product_set = category.product_set.all()
        default_products = category.default_products.all()

        context['products'] = (product_set | default_products).distinct()
        return context
