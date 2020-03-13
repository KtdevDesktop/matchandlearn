from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('tinderforeduapp.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace="social")),]

