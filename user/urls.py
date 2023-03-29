from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserLoginView,UserRegistrationView,UserProfileView

app_name = 'user'

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('registration/',UserRegistrationView.as_view(),name='registration'),
    path('profile/<int:pk>/',login_required(UserProfileView.as_view()),name='profile'),
    path('logout/', LogoutView.as_view(), name='logout')
]