"""djcommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from .views import index, login_view, logout_view, register_view
from products import urls as products_urls
from products import urls_cat
from carts import urls as carts_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='home_page'),
    url(r'^login$', login_view, name="login"),
    url(r'^logout$', logout_view, name="logout"),
    url(r'^register$', register_view, name="register"),
    url(r'^products/', include(products_urls)),
    url(r'^categories/', include(urls_cat)),
    url(r'^cart/', include(carts_urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
