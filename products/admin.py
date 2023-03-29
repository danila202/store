from django.contrib import admin
from django.db import models

from products.models import Product, ProductCategory,Basket
# Register your models here.
admin.site.register(ProductCategory)

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name','description','price','quantity','category')
    fields = ('name','description',('price','quantity'),'category')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('description','category')



class AdminBasket(admin.TabularInline):
    model = Basket
    fields = ('product','quantity')
    extra = 0



