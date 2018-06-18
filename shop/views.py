from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from shop.models import Category, Product, CartItem, Cart
from decimal import Decimal


# Create your views here.


def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    categories = Category.object.all()
    products = Product.object.all()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
    }
    return render(request, 'main.html', context)


def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    product = Product.object.get(slug=product_slug)
    context = {
        'product': product,
        'cart': cart,
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    category = Category.object.get(slug=category_slug)
    products_of_category = Product.object.filter(category=category)
    context = {
        'category': category,
        'products_of_category': products_of_category
    }
    return render(request, 'category.html', context)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.object.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    return JsonResponse({'cart_total':cart.items.count()})


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.object.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    return JsonResponse({'cart_total':cart.items.count()})


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.object.get(id=int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = int(qty) * cart_item.product.price
    cart_item.save()
    return JsonResponse({'cart_total':cart.items.count(), 'item_total': cart_item.item_total})
