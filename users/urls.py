from django.urls import path
from .views import LoginView, SignUpView

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login_page'),
    path('signup/', SignUpView.as_view(), name='signup'),

]
