from django.contrib import admin

from products.admin import AdminBasket

from .models import EmailVerification, User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('username', )
    inlines = (AdminBasket, )


@admin.register(EmailVerification)
class AdminEmailVerification(admin.ModelAdmin):
    list_display = ('uniq_code', 'user', 'expiration')
    fields = ('uniq_code', 'user', 'data_created', 'expiration')
    readonly_fields = ('data_created', )
