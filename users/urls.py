from django.urls import path
from .views import LoginView, SignUpView, ProfileView, LogoutView, DeleteProfileView, \
    UserDetailView, ContactView

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),

    path('show/<int:id>-<str:username>/', UserDetailView.as_view(), name='user-detail'),

]
