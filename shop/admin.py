from django.contrib import admin
from shop.models import Category, Brand, Product, CartItem, Cart
# Register your models here.


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)