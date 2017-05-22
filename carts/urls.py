from django.conf.urls import url
from carts.views import CartView, ItemCountView, CheckoutView

urlpatterns = [
    url(r'^$', CartView.as_view(), name='cart'),
    url(r'^count/', ItemCountView.as_view(), name='cart_count'),
    url(r'^checkout/', CheckoutView.as_view(), name='checkout'),
]

