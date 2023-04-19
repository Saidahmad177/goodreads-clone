from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from friend.models import Friends
from .forms import SignUpForm, ProfileUpdateForm, ContactForm
from django.contrib import messages

from .models import CustomUser, Contact


# User register view
class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('not-found'))
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

        if request.user.is_authenticated:
            return redirect(reverse('not-found'))
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
            messages.info(request, '❗ Wrong username or password. Please enter a correct username and password', extra_tags='danger')
            return render(request, 'users/login.html', {'form': form,})


# User logout view
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, 'You have logged out')
            return redirect('home_page')

        return redirect(reverse('not-found'))


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


class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/contact.html')

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            Contact.objects.create(
                user=request.user.username,
                name=name,
                email=email,
                message=message,
            )

            messages.success(request, 'Your message has been sent successfully')

            return redirect(reverse('users:contact'))

        else:
            messages.info(request, 'Please enter a valid value.', extra_tags='warning')
            return redirect(reverse('users:contact'))
