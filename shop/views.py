from __future__ import unicode_literals

from django.shortcuts import render
from shop.models import Category, Product


# Create your views here.


def base_view(request):
    categories = Category.object.all()
    products = Product.object.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'main.html', context)
