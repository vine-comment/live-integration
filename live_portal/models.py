from django.db import models

class Room(models.Model):
    platform_anchor = models.CharField(max_length=255, primary_key=True)
    anchor = models.CharField(max_length=128)
    tag = models.CharField(max_length=50)
    room_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    audience_count = models.IntegerField(default=0)
    platform = models.CharField(max_length=64)
    platform_prefix_url = models.CharField(max_length=128)
    #creation_time = models.DateTimeField(auto_now=False)
    modification_time = models.DateTimeField(auto_now=True)
    video_img_local_path = models.CharField(max_length=255)
