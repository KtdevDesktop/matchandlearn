from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.db import models


class Subject(models.Model):
    subject_name = models.TextField(max_length=200, blank=True)
    def __str__(self):
        return self.subject_name

class request_class(models.Model):
    request_list = models.TextField(max_length=200,blank=True)
class match_class(models.Model):
    match = models.TextField(max_length=200,blank=True)

class Userinfo(models.Model):
    name = models.TextField(max_length=200, blank=True)
    fullname = models.TextField(max_length=200, blank=True)
    lastname = models.TextField(max_length=200, blank=True)
    age = models.TextField(max_length=10,blank=True)
    school = models.TextField(max_length=200,blank=True)
    good_subject = models.ManyToManyField(Subject, related_name='Userinfos')
    request = models.ManyToManyField(request_class)
    match = models.ManyToManyField(match_class)
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    age = models.TextField(max_length=10, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
