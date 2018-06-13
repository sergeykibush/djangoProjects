from django.urls import path, re_path
from shop.views import base_view, category_view, product_view


urlpatterns = [
    path('', base_view, name='base'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    re_path(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
]
