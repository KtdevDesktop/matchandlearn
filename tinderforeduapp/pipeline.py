from .models import Userinfo, Profilepic
from django.contrib.auth.models import User
from social_core.pipeline.user import get_username as social_get_username
from datetime import date, datetime
user_email = ""

def get_email(backend, user, response, *args, **kwargs):
    global user_email
    if response.get('email') == None:
        user_email = (response.get('name')).split(" ")[0] + (response.get('name')).split(" ")[1]
    else:
        user_email = (response.get('email')).split("@")[0]

def user_profile_db(backend, user, response, *args, **kwargs):
    if not User.objects.filter(email=response.get('email')).exists():
        gender = ''
        birthdate = response.get('birthday')
        born = datetime.strptime(birthdate, '%m/%d/%Y')
        age = int((datetime.today() - born).days/365)
        if response.get('gender') == 'male':
            gender = 'Male'
        if response.get('gender') == 'female':
            gender = 'Female'
        if response.get('email') == None:
            user = Userinfo.objects.create(name=(response.get('name')).split(" ")[0] + (response.get('name')).split(" ")[1],
                                    school='',
                                    age=age,
                                    fullname=(response.get('name')).split(" ")[0],
                                    lastname=(response.get('name')).split(" ")[1],
                                    bio=gender, fb_link=response.get('link'))
        else:
            user = Userinfo.objects.create(name=(response.get('email')).split("@")[0],
                                school='',
                                age=age,
                                fullname=(response.get('name')).split(" ")[0],
                                lastname=(response.get('name')).split(" ")[1],
                                bio=gender, fb_link=response.get('link'))
        Profilepic.objects.create(user=user, images='default.png')

def get_username(strategy, details, backend, user=None, *args, **kwargs):
    result = social_get_username(strategy, details, backend, user=user, *args, **kwargs)
    result['username'] = user_email
    return result