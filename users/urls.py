from django.urls import path
from .views import LoginView, SignUpView, ProfileView, LogoutView, DeleteProfileView

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),

]
