from django.conf.urls import url
from products.views import CategoryListView, CategoryDetailView


urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name="category_list"),
    url(r'^(?P<pk>\d+)$', CategoryDetailView.as_view(), name="category_detail"),
]
