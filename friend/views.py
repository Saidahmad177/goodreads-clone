from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from friend.models import Friends
from users.models import CustomUser


class FriendsView(LoginRequiredMixin, View):
    def get(self, reqeust):
        followers = Friends.objects.filter(recipient=reqeust.user, accepted=True)
        following = Friends.objects.filter(requester=reqeust.user, accepted=True)
        context = {
            'followers': followers,
            'following': following,
            'reqeusts': Friends.objects.filter(recipient=reqeust.user)
        }

        return render(reqeust, 'friend/friends.html', context)

    def post(self, request):
        friend_id = request.POST.get('friend')
        friend = Friends.objects.get(id=friend_id)
        action = request.POST.get('action')

        if action == 'accept':
            friend.accepted = True
            friend.save()
            messages.success(request, f"{friend.requester} is now your friend")

        elif action == 'reject':
            friend.delete()
            messages.info(request, 'Request rejected')

        return redirect(reverse('friends:friends'))


class SendFriendRequestView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        recipient = CustomUser.objects.get(id=user_id)

        Friends.objects.create(
            requester=request.user,
            recipient=recipient
        )
        messages.success(request, 'Friend request sent')
        return redirect(reverse('users:user-detail',
                                kwargs={'id': recipient.id, 'username': recipient.username}))


# this is remove following (UnFollow)
class DeleteFriendView(LoginRequiredMixin, View):
    def get(self, request, id, username):
        user = CustomUser.objects.get(username=username)
        friends = Friends.objects.filter(requester=request.user, recipient=id)
        friends.delete()

        return redirect(reverse('users:user-detail', kwargs={'id': user.id, 'username': username}))


# this is remove follower
class RemoveFriendView(LoginRequiredMixin, View):
    def get(self, request, id, username):
        friends = Friends.objects.filter(requester=id, recipient=request.user)
        friends.delete()
        messages.info(request, f"You removed {username}")

        return redirect(reverse('friends:friends'))

