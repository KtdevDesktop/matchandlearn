# chat/views.py
from django.shortcuts import render
from .models import Savechat
def index(request):
    return render(request, 'chat/index.html', {})
def room(request, room_name):
    if Savechat.objects.filter(name=room_name).exists():
        test = Savechat.objects.get(name=room_name).chat
    else:
        test = ""
    return render(request, 'chat/room.html', {'room_name': room_name, 'test' : test} )

