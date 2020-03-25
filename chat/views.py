# chat/views.py
from django.shortcuts import render
from .models import Savechat
from django import db
from django.db import close_old_connections
from tinderforeduapp.models import  *
def index(request):
    return render(request, 'chat/index.html', {})
def room(request, room_name):
    splitlog = []
    log = ""
    user = room_name.split("_")
    usercheck1 = user[0]
    usercheck2 = user[1]
    username = request.user.username
    if Savechat.objects.filter(name=room_name,user1=usercheck1,user2=usercheck2).exists():
        if (Savechat.objects.get(name=room_name).user1 == username) or (Savechat.objects.get(name=room_name).user2 == username):
            log = Savechat.objects.get(name=room_name).chat
            splitlog = log.split("`~`~`~`~`~`")
            usercheck1 = Savechat.objects.get(name=room_name).user1
            usercheck2 = Savechat.objects.get(name=room_name).user2
    close_old_connections()
    db.connection.close()
    return render(request, 'chat/room.html', {'name':Userinfo.objects.get(name=request.user.username),'room_name': room_name,
                                                      'log': log,
                                                      'usercheck1': usercheck1,
                                                      'usercheck2': usercheck2,
                                                      'splitlog': splitlog})

