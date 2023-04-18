from .views import OrderCreateView

from django.urls import path

app_name = 'orders'

urlpatterns = [
    path('order-create/',OrderCreateView.as_view(),name='order-create'),

]