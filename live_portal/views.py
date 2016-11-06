#coding:utf-8

from django.views.generic import *
from django.http import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login

from models import *
from datetime import timedelta
from django.utils import timezone

from registration.signals import user_registered


def get_profile(user):
    try:
        return user.audience
    except:
        try:
            return user.anchor
        except:
            return None

# This callback is called by a registration signal.
def register_with_profile(sender, user, request, **kwargs):
    profile = Profile(user=user)
    profile.is_human = bool(request.POST["is_human"])
    profile.save()


# This callback is called by a registration signal.
def register_with_audience_profile(sender, user, request, **kwargs):
    profile = Audience(user=user)
    profile.save()


# Now a registered user is always a student.
user_registered.connect(register_with_audience_profile)

# ajax handler
def enter_room(request, room):
    if request.user.is_authenticated():
        audience = get_profile(request.user)
        room = Room.objects.filter(platform_anchor=room)[0]
        rv = Rvisit.objects.get_or_create(audience=audience, room=room)[0]
        rv.visit_count += 1
        rv.save()
        count = audience.recent_visited.count()
        if count >= 10:
            stale = Rvisit.objects.all().order_by('visit_time')[0]
            stale.delete()

    return HttpResponse(status=200)

def follow_room(request, room):
    if request.user.is_authenticated():
        audience = get_profile(request.user)
        room = Room.objects.filter(platform_anchor=room)[0]
        rv,ret = Rfollow.objects.get_or_create(audience=audience, room=room)
        rv.save()

    return HttpResponse(status=200)

def unfollow_room(request, room):
    if request.user.is_authenticated():
        audience = get_profile(request.user)
        room = Room.objects.filter(platform_anchor=room)[0]
        rv = Rfollow.objects.filter(audience=audience, room=room)
        if rv:
            rv.delete()
            return HttpResponse(status=200)

    return HttpResponse(status=404)

# views
class ShowView(TemplateView):
    template_name = 'live_portal_show.html'
    merged_tag_mapping = {
        u'户外': [u'Outdoor', u'鱼行天下', u'户外直播', u'全民户外', u'元气领域'],
        u'秀场': [u'全民星秀', u'娱乐联萌', u'鱼音绕梁', u'鱼秀', u'二次元'],
        u'体育': [u'体育频道', u'体育竞技'],
        u'主机游戏': [u'单机主机', u'主机游戏', u'单机游戏'],
        u'放映厅': [u'一起看', u'第九放映室'],
        u'': [],
    }

    def get(self, request, tag):
        if not tag or tag == u'所有直播':
            # rooms = Room.objects.all()
            # NOTE: MySQL generate timestamp with UTC+8 timezone, but here timezone.now() gets UTC.
            rooms = Room.objects.all()
            tag = u'所有直播'
        elif tag in self.merged_tag_mapping:
            rooms = Room.objects.filter(tag__in=self.merged_tag_mapping[tag])
        else:
            rooms = Room.objects.filter(tag=tag)

        rooms_top = rooms.filter(modification_time__gte=timezone.now()+timedelta(hours=7, minutes=49)).order_by('audience_count').reverse()

        page_index = request.GET.get('page', 1)
        p = Paginator(rooms_top, 120)
        try:
            p_rooms = p.page(page_index)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            p_rooms = p.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            p_rooms = p.page(p.num_pages)

        return render(request, self.template_name,
                {'tag':tag, 'p_rooms':p_rooms})

class HomeView(TemplateView):
    template_name = 'live_portal_home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = get_profile(request.user)
            #rooms_top = user.recent_visited.filter(modification_time__gte=timezone.now()+timedelta(hours=240)).order_by('audience_count').reverse()
            rooms_recent_visited_top = user.recent_visited.all() #TODO: use through model, so we will have timestamp
            rooms_follows_top = user.follows.all() #TODO: use through model, so we will have timestamp

            page_index = request.GET.get('page', 1)
            p_recent_visited = Paginator(rooms_recent_visited_top, 12)
            try:
                p_recent_visited_rooms = p_recent_visited.page(page_index)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                p_recent_visited_rooms = p_recent_visited.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                p_recent_visited_rooms = p_recent_visited.page(p_recent_visited.num_pages)

            p_follows = Paginator(rooms_follows_top, 12)
            try:
                p_follows_rooms = p_follows.page(page_index)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                p_follows_rooms = p_follows.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                p_follows_rooms = p_follows.page(p_follows.num_pages)

            return render(request, self.template_name,
                    {'p_recent_visited_rooms':p_recent_visited_rooms,
                     'p_follows_rooms':p_follows_rooms})
        else:
            return HttpResponseRedirect("/show/")

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
            else:
                login(request, user)
                # Return a 'disabled account' error message
        else:
            # Return an 'invalid login' error message.
            return HttpResponseRedirect("/auth/")

        return HttpResponseRedirect("/show/")


class UserFollowsView(TemplateView):
    template_name = 'live_portal_user_follows.html'

    def get(self, request, *args, **kwargs):
        profile = get_profile(request.user)

        fxy = Room.objects.get(anchor='trevor行云')
        profile.follows.add(fxy)
        rooms = profile.follows.all()

        # debug
        print(rooms.values)

        return render(request, self.template_name, {'rooms': rooms})
