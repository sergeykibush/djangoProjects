from django.urls import path, include
from shop.views import base_view


urlpatterns = [
    path('', base_view, name='base'),

]
