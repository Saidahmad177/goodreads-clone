from django.urls import path
from .views import BooksListView, DetailView, DeleteReview, EditReview

app_name = 'book'
urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('<slug:slug>', DetailView.as_view(), name='detail_view'),
    path('<slug:slug>/<int:review_id>/delete/', DeleteReview.as_view(), name='delete-review'),
    path('<slug:slug>/<int:review_id>/edit/', EditReview.as_view(), name='edit-review'),


]
