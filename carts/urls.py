from django.conf.urls import url, include
from carts.views import CartView

urlpatterns = [
    url(r'^$', CartView.as_view(), name='cart'),

]

