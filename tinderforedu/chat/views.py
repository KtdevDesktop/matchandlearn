# chat/views.py
from django.shortcuts import render
from tinderforeduapp.models import User

def index(request):
    return render(request, 'chat/index.html', {})
def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})