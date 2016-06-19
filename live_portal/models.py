from django.db import models

class Room(models.Model):
    anchor = models.CharField(max_length=100)
    tag = models.CharField(max_length=50)
    room_name = models.CharField(max_length=100)
    platform_name = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now=False)
    url = models.CharField(max_length=200)
    audience_c = models.IntegerField(default=0)
