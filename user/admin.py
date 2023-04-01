from django.contrib import admin

# Register your models here.

from .models import User,EmailVerification
from products.admin import AdminBasket

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (AdminBasket,)


@admin.register(EmailVerification)
class AdminEmailVerification(admin.ModelAdmin):
    list_display = ('uniq_code','user','expiration')
    fields = ('uniq_code','user','data_created','expiration')
    readonly_fields = ('data_created',)



