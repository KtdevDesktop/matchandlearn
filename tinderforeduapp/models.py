from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Subject(models.Model):
    subject_name = models.TextField(max_length=200, blank=True)
    subject_keep = models.TextField(max_length=200, blank=True)
    def __str__(self):
        return self.subject_name


class request_class(models.Model):
    request_list = models.TextField(max_length=200,blank=True)
    request_message = models.TextField(max_length=600,blank=True)
    whorecive = models.TextField(max_length=200,blank=True)
    def __str__(self):
        return self.request_list
class match_class(models.Model):
    match = models.TextField(max_length=200,blank=True)
    youself = models.TextField(max_length=200,blank=True)
    def __str__(self):
        return self.match

class Userinfo(models.Model):
    name = models.TextField(max_length=200, blank=True)
    fullname = models.TextField(max_length=200, blank=True)
    lastname = models.TextField(max_length=200, blank=True)
    age = models.TextField(max_length=10,blank=True)
    school = models.TextField(max_length=200,blank=True)
    schoolkey = models.TextField(max_length=200,blank=True)
    bio = models.TextField(blank=True)
    fb_link = models.TextField(null=True)
    good_subject = models.ManyToManyField(Subject, related_name='Userinfos',blank=True)
    request = models.ManyToManyField(request_class,blank=True)
    match = models.ManyToManyField(match_class,blank=True)
    match_request = models.IntegerField(default=0)
    massage_list = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    def read(self):
        self.match_request = 0
        self.save()
    def notify(self):
        self.match_request = self.match_request + 1
        self.save()

    def denotify(self):
        self.match_request = self.match_request - 1
        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Userinfo,on_delete=models.CASCADE,related_name='comments',null=True)
    name = models.CharField(max_length=80,null=True)
    comment = models.CharField(max_length=500,null=True)
    star = models.CharField(max_length=500,null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True,null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment to {} by {}'.format(self.post, self.name)

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
class Profilepic(models.Model):
    user = models.OneToOneField(Userinfo, on_delete=models.CASCADE)
    images = models.ImageField(default='default.png',upload_to='media')


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
