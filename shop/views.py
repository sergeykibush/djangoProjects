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


def product_view(request, product_slug):
    product = Product.object.get(slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    category = Category.object.get(slug=category_slug)
    context = {
        'category': category
    }
    return render(request, 'category.html', context)