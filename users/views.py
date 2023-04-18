from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from friend.models import Friends
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib import messages

from .models import CustomUser


# User register view
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

            messages.success(request, 'Congratulations 🎉, You have successfully registered')

            return redirect('users:login')

        else:

            context = {
                'form': form,
                'errors': form.errors

            }
            return render(request, 'users/register.html', context)


# User login View
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
            return render(request, 'users/login.html', {
                'form': form,
                'invalid': True,
            })


# User logout view
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have logged out')
        return redirect('home_page')


# User profile View
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        follower = Friends.objects.filter(recipient=request.user, accepted=True)
        following = Friends.objects.filter(requester=request.user, accepted=True)

        context = {
            'form': form,
            'followers': follower,
            'following': following,
        }

        return render(request, 'users/profile.html', context)

    def post(self, request):
        form = ProfileUpdateForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully update profile')
            return redirect('users:profile')

        return render(request, 'users/profile.html', {'form': form})


# Delete account View
class DeleteProfileView(LoginRequiredMixin, View):

    def get(self, reqeust):
        reqeust.user.delete()
        messages.info(reqeust, 'You are deleted account!')
        return redirect('home_page')


class UserDetailView(LoginRequiredMixin, View):
    def get(self, request, id, username):
        user = CustomUser.objects.get(id=id, username=username)

        pending = Friends.objects.filter(requester=request.user, recipient=user, accepted=False).exists()
        is_follower = Friends.objects.filter(requester=user, recipient=request.user, accepted=True).exists()
        is_following = Friends.objects.filter(requester=request.user, recipient=user, accepted=True).exists()

        follower = Friends.objects.filter(recipient=id, accepted=True)
        following = Friends.objects.filter(requester=id, accepted=True)

        context = {
            'user_detail': user,
            'is_following': is_following,
            'is_follower': is_follower,
            'pending': pending,
            'follower': follower,
            'following': following,
        }

        return render(request, 'users/user_detail.html', context)

