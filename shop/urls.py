from django.urls import path, re_path
from shop.views import base_view, category_view, product_view, cart_view, add_to_cart_view, remove_from_cart_view, change_item_qty


urlpatterns = [
    path('', base_view, name='base'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    re_path(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    re_path(r'^add_to_cart/$', add_to_cart_view, name='add_to_cart'),
    re_path(r'^remove_from_cart/$', remove_from_cart_view, name='remove_from_cart'),
    re_path(r'^cart/$', cart_view, name='cart'),
    re_path(r'^change_item_qty/$', change_item_qty, name='change_item_qty'),

]
