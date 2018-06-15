from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from shop.models import Category, Product, CartItem, Cart


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


def add_to_cart_view(request, product_slug):
    product = Product.object.get(slug=product_slug)
    new_item, _ = CartItem.object.get_or_create(product=product, item_total=product.price)
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
    if new_item not in cart.items.all():
        cart.items.add(new_item)
        cart.save()
    return HttpResponseRedirect('/cart/')


def remove_from_cart_view(request, product_slug):
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
    for cart_item in cart.items.all():
        if cart_item.product == product:
            cart.items.remove(cart_item)
            cart.save()
            return HttpResponseRedirect('/cart/')
