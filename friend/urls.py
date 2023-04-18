from django.urls import path
from .views import FriendsView, SendFriendRequestView, \
    DeleteFriendView, RemoveFriendView

app_name = 'friends'
urlpatterns = [
    path('', FriendsView.as_view(), name='friends'),
    path('<int:id>-<str:username>/remove-friend/', RemoveFriendView.as_view(), name='remove-friend'),

    path('<int:user_id>/send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('<int:id>-<str:username>/delete', DeleteFriendView.as_view(), name='delete-friend'),

]
