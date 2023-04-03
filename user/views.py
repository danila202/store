from django.contrib.auth.views import LoginView
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth,messages
from django.urls import reverse,reverse_lazy
from django.views.generic.base import TemplateView
from user.form import UserLoginForm,UserRegistrationForm,UserProfileForm
from django.views.generic import CreateView,UpdateView
from products.models import Basket
from django.contrib.messages.views import SuccessMessageMixin
from .models import User,EmailVerification
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
    success_message = 'Вы успешно зарегистрировались! Для подтверждения почты перейдите по ссылке, высланной на указанный почтовый адрес'
    title = 'Store - Регистрация'



class UserProfileView(TitleMixin,UpdateView):
    model = User
    template_name = 'user/profile.html'
    form_class = UserProfileForm
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('user:profile',args=(self.object.id,))

class EmailVerificationView(TitleMixin,TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'user/email_verification.html'

    def get(self, request, *args, **kwargs):
        uniq_code = kwargs['uniq_code']
        user = User.objects.get(email=kwargs['email'])
        email_verify = EmailVerification.objects.filter(user=user,uniq_code=uniq_code)
        if email_verify.exists() and not email_verify.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView,self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))




