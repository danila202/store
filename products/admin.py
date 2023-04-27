from django.contrib import admin

from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stripe_product_price_id', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'stripe_product_price_id', 'quantity'), 'category')
    search_fields = ('name', )
    ordering = ('name', )
    readonly_fields = ('description', 'category')


class AdminBasket(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0
