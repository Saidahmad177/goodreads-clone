from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib import messages


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form,
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('users:login')

        else:
            context = {
                'form': form,
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home_page')

        else:
            return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have logged out')
        return redirect('home_page')


class ProfileView(LoginRequiredMixin, View):
    # def get(self, request):
    #     return render(request, 'users/profile.html', {'user': request.user})

    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'users/profile.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully update profile')
            return redirect('users:profile')

        return render(request, 'users/profile.html', {'form': form})

