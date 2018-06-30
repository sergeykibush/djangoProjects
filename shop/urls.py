from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from shop.views import (
base_view,
category_view,
product_view,
cart_view,
add_to_cart_view,
remove_from_cart_view,
change_item_qty,
checkout_view,
profile_view,
registration_view,
login_view
)

urlpatterns = [
    path('', base_view, name='base'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    re_path(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    re_path(r'^add_to_cart/$', add_to_cart_view, name='add_to_cart'),
    re_path(r'^remove_from_cart/$', remove_from_cart_view, name='remove_from_cart'),
    re_path(r'^cart/$', cart_view, name='cart'),
    re_path(r'^change_item_qty/$', change_item_qty, name='change_item_qty'),
    re_path(r'^checkout/$', checkout_view, name='checkout'),
    path('thanks/', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    path('profile/', profile_view, name = 'profile'),
    path('registration/', registration_view, name = 'registration'),
    path('login/', login_view, name = 'login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base')), name = 'logout')
]
