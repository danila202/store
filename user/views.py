from django.contrib.auth.views import LoginView
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth,messages
from django.urls import reverse,reverse_lazy
from user.form import UserLoginForm,UserRegistrationForm,UserProfileForm
from django.views.generic import CreateView,UpdateView
from products.models import Basket

from .models import User



class UserLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm


class UserRegistrationView(CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - Регистрация'
        return context


class UserProfileView(UpdateView):
    model = User
    template_name = 'user/profile.html'
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('user:profile',args=(self.object.id,))


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))



# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user,data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#     content = {'form':form,
#                'baskets': Basket.objects.all(),
#                }
#     return render(request,'user/profile.html',content)
# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Вы успешно зарегистрированы')
#             return HttpResponseRedirect(reverse('user:login'))
#     else:
#        form = UserRegistrationForm()
#     context = {'form': form}
#
#     return render(request, 'user/registration.html',context)

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=user,password=password)
#             if user:
#                 auth.login(request,user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form':form}
#     return render(request,'user/login.html',context)