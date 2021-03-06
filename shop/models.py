# from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
# Create your models here.


class Category(models.Model):
    object = models.Manager()

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(instance.name, reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Brand(models.Model):
    object = models.Manager()

    name = models.CharField(max_length=100)
    web_site = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class ProductManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter()


class Product(models.Model):
    object = ProductManager()

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=124)
    slug = models.SlugField()
    description = models.TextField()
    size = models.CharField(max_length=10, choices=(('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')), null=True)
    dimensions = models.CharField(max_length=40, null=True)
    liters = models.IntegerField(null=True)
    weight = models.CharField(max_length=20, null=True)
    covers = models.CharField(max_length=10, choices=(('1', '1'), ('2', '2')), null=True)
    material = models.CharField(max_length=100, choices=(
        ('Оксфорд', 'Оксфорд'),
        ('Оксфорд плотный 600d', 'Оксфорд плотный 600d'),
        ('Микро-рогожка, Шотландия клетка, велюр Нью-Йорк(принт)', 'Микро-рогожка, Шотландия клетка, велюр Нью-Йорк(принт)'),
        ('Кожзам Зевс, Плетенка 3D', 'Кожзам Зевс, Плетенка 3D'),
        ('Хлопок', 'Хлопок'),
        ('Велюр Кордрой', 'Велюр Кордрой'),
        ('Велюр Мольберт цветы, Кристалл', 'Велюр Мольберт цветы, Кристалл'),
        ), null=True)
    image = models.ImageField(upload_to="images/products", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    marketing_price = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


class CartItem(models.Model):
    object = ProductManager()

    product = models.ForeignKey(Product, on_delete=True)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __unicode__(self):
        return "Cart item for product {0}".format(self.product.title)


class Cart(models.Model):
    object = ProductManager()

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __unicode__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.object.get(slug=product_slug)
        new_item, _ = CartItem.object.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()
        return

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.object.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart_item.delete()
                cart.save()
        return

    def change_qty(self,qty, item_id):
        cart = self
        cart_item = CartItem.object.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * cart_item.product.price
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save


ORDER_STATUS_CHOISES = {
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')
}
class Order(models.Model):
    object = ProductManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=True)
    items = models.ForeignKey(Cart, on_delete=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=40)
    address = models.CharField(max_length=225)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')), default='Самовывоз')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOISES, default='Принят в обработку')

    def __unicode__(self):
        return "Заказ №{0}".format(str(self.id))
