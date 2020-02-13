from django.contrib import admin
from .models import Profile, Userinfo
from chat.models import Savechat
admin.site.register(Profile)
admin.site.register(Userinfo)
admin.site.register(Savechat)
# Register your models here.
