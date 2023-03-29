from django.contrib.auth.views import LoginView
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth,messages
from django.urls import reverse,reverse_lazy
from user.form import UserLoginForm,UserRegistrationForm,UserProfileForm
from django.views.generic import CreateView,UpdateView
from products.models import Basket
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from common.views import TitleMixin

class UserLoginView(TitleMixin,LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'



class UserRegistrationView(TitleMixin,SuccessMessageMixin,CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    success_message = 'Вы успешно зарегистрировались!'
    title = 'Store - Регистрация'



class UserProfileView(TitleMixin,UpdateView):
    model = User
    template_name = 'user/profile.html'
    form_class = UserProfileForm
    title = 'Store - Личный кабинет'

    def get_context_data(self):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('user:profile',args=(self.object.id,))
