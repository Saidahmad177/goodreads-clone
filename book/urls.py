from django.urls import path
from .views import BooksListView, DetailView, DeleteReview, EditReview, MyReviewsView, \
    EditMyReview, delete_my_review

app_name = 'book'

urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('<slug:slug>', DetailView.as_view(), name='detail_view'),
    path('my-reivews/', MyReviewsView.as_view(), name='my-reviews'),
    path('<int:review_id>/review-delete/', delete_my_review, name='delete-my-review'),
    path('<int:review_id>/my-review-edit/', EditMyReview.as_view(), name='edit-my-review'),

    path('<slug:slug>/<int:review_id>/delete/', DeleteReview.as_view(), name='delete-review'),
    path('<slug:slug>/<int:review_id>/edit/', EditReview.as_view(), name='edit-review'),

]


