from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Subject(models.Model): #create subject model
    subject_name = models.TextField(max_length=200, blank=True) #Collect a subject data when user add it
    subject_keep = models.TextField(max_length=200, blank=True) #Collect a subject_name value in lower case for easily to search
    def __str__(self):
        return self.subject_name


class request_class(models.Model):#create request model
    request_list = models.TextField(max_length=200,blank=True)#Collect a name who sent a request
    request_message = models.TextField(max_length=600,blank=True)#Collect about me data
    whorecive = models.TextField(max_length=200,blank=True)#Collect a name who will recive a request
    def __str__(self):
        return self.request_list
class match_class(models.Model):#creat match model
    who_matched = models.TextField(max_length=200, blank=True) #Collect a name who matched with user
    who_request = models.TextField(max_length=200, blank=True)#Collect a name who sent a request
    def __str__(self):
        return self.who_matched

class Userinfo(models.Model):#create user information model
    name = models.TextField(max_length=200, blank=True)#Collect a username data
    firstname = models.TextField(max_length=200, blank=True)#Collect a first name
    lastname = models.TextField(max_length=200, blank=True)#Collect a last name
    age = models.TextField(max_length=10,blank=True)#Collect a age
    school = models.TextField(max_length=200,blank=True)#Collect a school name
    schoolkey = models.TextField(max_length=200,blank=True)#get a value from school variable a convert to upper case for easily to search
    bio = models.TextField(blank=True)#Collect a gender
    fb_link = models.TextField(null=True)#Collect a facebook link
    good_subject = models.ManyToManyField(Subject, related_name='Userinfos',blank=True)#enable to link this model to subject model
    request = models.ManyToManyField(request_class,blank=True)#enable to link this model to request model
    match = models.ManyToManyField(match_class,blank=True)#enable to link this model to match model
    match_request = models.IntegerField(default=0)#Collect amount of notify when you have a request from someone
    massage_list = models.IntegerField(default=0)#Collect amount of notify when you have a massage from someone

    def __str__(self):
        return self.name
    def read(self):#its mean when you go to request list then amount of notify will be zero
        self.match_request = 0
        self.save()
    def notify(self):#when you have request amount of notify should be increase
        self.match_request = self.match_request + 1
        self.save()

    def denotify(self):#when someone cancel request amount of notify should be decrease
        self.match_request = self.match_request - 1
        self.save()

class Comment(models.Model):#create comment model
    post = models.ForeignKey(Userinfo,on_delete=models.CASCADE,related_name='comments',null=True)#link this model to userinfo
    name = models.CharField(max_length=80,null=True)#Collect a name who comment you
    comment = models.CharField(max_length=500,null=True)#Collect a comment massage
    star = models.CharField(max_length=500,null=True)#Collect a score
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True,null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment to {} by {}'.format(self.post, self.name)

class Profile(models.Model):#create a profile model,this model is same Userinfo model,this model is create for when user register then this model keep a information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    age = models.TextField(max_length=10, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
class Profile_pic(models.Model):#this model create for Profile picture
    user = models.OneToOneField(Userinfo, on_delete=models.CASCADE)#Collect a first name
    images = models.ImageField(default='default.png',upload_to='media')#Collect a picture


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
