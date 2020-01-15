from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models


class Subject(models.Model):
    subject_name = models.TextField(max_length=200, blank=True)
    def __str__(self):
        return self.subject_name


class Userinfo(models.Model):
    name = models.TextField(max_length=200, blank=True)

    good_subject = models.ManyToManyField(Subject)
    def __str__(self):
        return self.name


# Create your models here.
