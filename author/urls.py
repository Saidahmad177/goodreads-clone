from django.urls import path
from .views import AuthorListView, AuthorDetailView

app_name = 'author'
urlpatterns = [
    path('', AuthorListView.as_view(), name='author_list'),
    path('<int:id>/', AuthorDetailView.as_view(), name='author-detail-page'),
]
