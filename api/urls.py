from django.urls import path
from .views import BookListReviewApiView, BookReviewDetailApiView

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()


app_name = 'api'
urlpatterns = [
    path('reviews/', BookListReviewApiView.as_view(), name='book_review'),
    path('reviews/<int:id>/', BookReviewDetailApiView.as_view(), name='review_detail'),

]
