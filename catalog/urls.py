from django.conf.urls import url

from catalog.views import ProductsPage, FilteredProductsPage
from . import views

app_name = 'catalog'
urlpatterns = [
    # url(r'^$', views.catalog, name='products_page'),
    url(r'^(?P<category_slug>[\w-]+)_(?P<subcategory_slug>[\w-]+)$', ProductsPage.as_view(), name='products_page'),
url(r'^(?P<category_slug>[\w-]+)_(?P<subcategory_slug>[\w-]+)/filter/(?P<extra_params>[\w\D]+)$',
        FilteredProductsPage.as_view(), name='filtered_products')
]
