from django.db import models

class Savechat(models.Model):
    name = models.TextField(blank=True)
    user1 = models.TextField(blank=True)
    user2 = models.TextField(blank=True)
    chat = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name