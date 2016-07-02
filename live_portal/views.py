#coding:utf-8

from django.views.generic import *
from django.http import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from live_portal.models import *
from datetime import timedelta
from django.utils import timezone


class ShowView(TemplateView):
    template_name = 'live_portal_show.html'

    def get(self, request, tag):
        if not tag or tag == 'all':
            # rooms = Room.objects.all()
            # NOTE: MySQL generate timestamp with UTC+8 timezone, but here timezone.now() gets UTC.
            rooms = Room.objects.filter(modification_time__gte=timezone.now()+timedelta(hours=7)).order_by('audience_count').reverse()[:100]
            tag = u'所有直播'
        else:
            rooms = Room.objects.filter(tag=tag, modification_time__gte=timezone.now()+timedelta(hours=7)).order_by('audience_count').reverse()[:100]

        return render(request, self.template_name,
                {'tag':tag, 'rooms':rooms})

class HomeView(TemplateView):
    template_name = 'live_portal_show.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/show/");
