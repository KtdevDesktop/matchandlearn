
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('tinderforeduapp/', include('tinderforeduapp.urls')),
    path('admin/', admin.site.urls),


]
