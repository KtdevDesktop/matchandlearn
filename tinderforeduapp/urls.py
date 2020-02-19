from django.urls import path

from .  import views

from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf.urls import include

from . import views as core_views

app_name = 'tinder'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('<int:user_id>/your_subject/', views.your_subject_page, name ='your_subject'),
    path('<int:user_id>/select_delete/', views.select_delete, name ='select_delete'),
    path('login/', LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='/tinderforeduapp/login'), name="logout"),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('<int:user_id>/profile/',views.another_profile,name='profile'),
    path('chat/', include('chat.urls')),
    path('<int:user_id>/match/',views.match,name="match"),
    path('<int:user_id>/Unmatched/',views.Unmatched,name="unmatched"),
    path('<int:user_id>/match_request/',views.match_request,name="match_request"),
    path('<int:user_id>/profile_accept/',views.profile_accept,name="profile_accept"),
    path('<int:user_id>/students_list/',views.students_list,name="students_list"),
    path('<int:user_id>/watch_profile',views.watch_profile,name="watch_profile"),
]