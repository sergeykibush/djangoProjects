from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from shop.models import Category, Product, CartItem, Cart, Order
from decimal import Decimal
from shop.forms import OrderForms, RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate



# Create your views here.


def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = CartItem.object.count()
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
        request.session['total'] = CartItem.object.count()
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
        request.session['total'] = CartItem.object.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save
    context = {
        'cart': cart,
        'cart_total':CartItem.object.count()
    }

    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = CartItem.object.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.object.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save
    return JsonResponse({'cart_total':CartItem.object.count(), 'cart_total_price': cart.cart_total,})


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = CartItem.object.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.object.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save
    return JsonResponse({'cart_total':CartItem.object.count(), 'cart_total_price': cart.cart_total,})


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = CartItem.object.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.object.get(id=int(item_id))
    return JsonResponse({
        'cart_total':CartItem.object.count(),
        'item_total': cart_item.item_total,
        'cart_total_price': cart.cart_total,
        })


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.object.get(id=cart_id)
        request.session['total'] = CartItem.object.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.object.get(id=cart_id)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save
    form = OrderForms(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        print(buying_type)
        new_order = Order.object.create(
            user = request.user,
            items = cart,
            total = cart.cart_total,
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            address = address,
            buying_type = buying_type,
            comments = comments,
        )
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thanks'))
    context = {
        'cart': cart,
        'cart_total':CartItem.object.count(),
        'form': form
    }
    return render(request, 'checkout.html', context)


def profile_view(request):
    order = Order.object.filter(user=request.user).order_by('-id')
    context = {
        'order': order
    }
    return render(request, 'profile.html', context)
def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'login.html', context)
