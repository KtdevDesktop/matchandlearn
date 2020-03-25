from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from tinderforedu import settings

urlpatterns = [
    path('', include('tinderforeduapp.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace="social")),] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

