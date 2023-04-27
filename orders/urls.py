from .views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, OrderListView, OrderDetailView

from django.urls import path

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order-success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order-canceled'),
    path('', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),

]
