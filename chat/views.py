# chat/views.py
from django.shortcuts import render
from .models import Savechat
def index(request):
    return render(request, 'chat/index.html', {})
def room(request, room_name):
    log = ""
    usercheck1 = ""
    usercheck2 = ""
    username = request.user.username
    if Savechat.objects.filter(name=room_name).exists():
        if (Savechat.objects.get(name=room_name).user1 == username) or (Savechat.objects.get(name=room_name).user2 == username):
            log = Savechat.objects.get(name=room_name).chat
            usercheck1 = Savechat.objects.get(name=room_name).user1
            usercheck2 = Savechat.objects.get(name=room_name).user2
    return render(request, 'chat/room.html', {'room_name': room_name, 'log' : log, 'usercheck1' : usercheck1, 'usercheck2' : usercheck2} )

