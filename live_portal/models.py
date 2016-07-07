#coding:utf-8

from django.db import models
from django.conf import settings


class Room(models.Model):
    platform_anchor = models.CharField(max_length=255, primary_key=True)
    anchor = models.CharField(max_length=128)
    tag = models.CharField(max_length=50)
    room_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    audience_count = models.IntegerField(default=0)
    platform = models.CharField(max_length=64)
    platform_prefix_url = models.CharField(max_length=128)
    # creation_time = models.DateTimeField(auto_now=False)
    modification_time = models.DateTimeField(auto_now=True)
    video_img_local_path = models.CharField(max_length=255)


# This class is to keep compability with other apps
# which use original settings.AUTH_USER_MODEL model.
class Profile(models.Model):
    # OneToOneField
    location = models.CharField(max_length=140, blank=True, null=True)
    gender = models.CharField(max_length=140, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='head_sculpture', blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)  # date of birth
    # phone = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    # is_human = models.BooleanField()

    # Status
    status = models.BooleanField(blank=True)
    last_login_ip = models.IPAddressField(blank=True, null=True)
    last_login_date = models.DateTimeField(blank=True, null=True)

    # Points
    usable_points = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    biggest_points = models.IntegerField(default=0)
    last_visit = models.DateTimeField(auto_now=True, null=True)

    # Profile Statistics Area:
    longest_streak = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    room_follow_cnt = models.IntegerField(default=0)

    @property
    def is_audience(self):
        try:
            self.audience
            return True
        except Audience.DoesNotExist:
            return False

    def __unicode__(self):
        return u'Profile of user: %s' % self.user

    class Meta:
        abstract = True


class Audience(Profile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="audience")
    follows = models.ManyToManyField(Room)


class Anchor(Audience):
    pass
