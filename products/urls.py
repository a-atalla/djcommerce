from django.conf.urls import url
from products.views import ProductListView, ProductDetailView, VariationListView


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name="product_list"),
    url(r'^(?P<pk>\d+)$', ProductDetailView.as_view(), name="product_detail"),
    url(r'^(?P<pk>\d+)/inventory$', VariationListView.as_view(), name="product_inventory"),

]
