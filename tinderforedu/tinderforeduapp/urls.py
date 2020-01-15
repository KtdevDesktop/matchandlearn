

from django.urls import path

from .  import views

app_name = 'tinder'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('<int:user_id>/your_subject/', views.your_subject_page, name ='your_subject'),
    path('<int:user_id>/your_subject/', views.select_delete, name ='select_delete'),
]