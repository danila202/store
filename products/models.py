from django.db import models
from django.conf import settings

from user.models import User

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_product_price_id = models.CharField(max_length=250, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Продукт : {self.name}| Категория :{self.category.name} '

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            product_stripe_product = self.create_stripe_price()
            self.stripe_product_price_id = product_stripe_product['id']

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product(self):
        product_name = stripe.Product.create(name=self.name)
        return product_name

    def create_stripe_price(self):
        product_price = stripe.Price.create(
            product=self.create_stripe_product()['id'], unit_amount=round(self.price*100), currency="rub"
        )
        return product_price


class BasketQuarySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def fill_stripe(self):
        line_items = []
        for item in self:
            product = {
                'price': item.product.create_stripe_price(),
                'quantity': item.quantity
            }
            line_items.append(product)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuarySet.as_manager()

    def __str__(self):
        return f'Корзина для  {self.user.email} | Продукт: {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def to_json(self):
        basket_item = {
            'product': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item

