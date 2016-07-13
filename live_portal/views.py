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
# XXX move this function to a meaningful file.
def register_with_profile(sender, user, request, **kwargs):
    profile = Profile(user=user)
    profile.is_human = bool(request.POST["is_human"])
    profile.save()


# This callback is called by a registration signal.
# XXX move this function to a meaningful file.
def register_with_audience_profile(sender, user, request, **kwargs):
    profile = Audience(user=user)
    profile.save()


# Now a registered user is always a student.
user_registered.connect(register_with_audience_profile)

# ajax handler
def enter_room(request, anchor):
    #platform_anchor = request.POST['anchor']
    if request.user.is_authenticated():
        user = get_profile(request.user)
        user.recent_visited.add(anchor)
        user.save()
        print "xxxxxxx:", anchor

    return HttpResponse(status=200)

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

        rooms_top = rooms.filter(modification_time__gte=timezone.now()+timedelta(hours=7)).order_by('audience_count').reverse()

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
    template_name = 'live_portal_show.html'

    def get(self, request, *args, **kwargs):
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
