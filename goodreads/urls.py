from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import home_page, SearchView

urlpatterns = [
    path('', home_page, name='home_page'),
    path('search/', SearchView.as_view(), name='search'),
    path('users/', include('users.urls')),
    path('books/', include('book.urls')),

    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
