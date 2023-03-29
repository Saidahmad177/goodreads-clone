from django.urls import path
from .views import BooksListView, DetailView

app_name = 'book'
urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('<slug:slug>', DetailView.as_view(), name='detail_view'),

]
