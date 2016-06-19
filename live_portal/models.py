from django.db import models

class Room(models.Model):
    anchor = models.CharField(max_length=100)
    tag = models.CharField(max_length=50)
    room_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    audience_c = models.CharField(max_length=100)
