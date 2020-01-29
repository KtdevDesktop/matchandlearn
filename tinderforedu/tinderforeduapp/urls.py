from django.urls import path

from .  import views

from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from . import views as core_views

app_name = 'tinder'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('<int:user_id>/your_subject/', views.your_subject_page, name ='your_subject'),
    path('<int:user_id>/select_delete/', views.select_delete, name ='select_delete'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='/tinderforeduapp/'), name="logout"),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('signup/home.html', views.home_page, name='home')
]
