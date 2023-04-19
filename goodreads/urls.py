from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import home_page, SearchView, landing_page, page_404


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', home_page, name='home_page'),
    path('search/', SearchView.as_view(), name='search'),
    path('user/', include('users.urls')),
    path('books/', include('book.urls')),
    path('api/', include('api.urls')),
    path('authors/', include('author.urls')),
    path('not-found/', page_404, name='not-found'),
    path('friend/', include('friend.urls')),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
