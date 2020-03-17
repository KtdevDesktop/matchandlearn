from .models import Userinfo
from django.contrib.auth.models import User
def user_profile_db(backend, user, response, *args, **kwargs):
    if not User.objects.filter(email=response.get('email')).exists():
        Userinfo.objects.create(name=(response.get('name')).split(" ")[0] + (response.get('name')).split(" ")[1],
                                school='',
                                age='',
                                fullname=(response.get('name')).split(" ")[0],
                                lastname=(response.get('name')).split(" ")[1],
                                bio='')