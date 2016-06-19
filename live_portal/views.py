#coding:utf-8

from django.views.generic import *
from django.http import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from live_portal.models import *

class ShowView(TemplateView):
    template_name = 'live_portal_show.html'

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('tag',None)
        if not tag:
            rooms = Room.objects.all()
        else:
            rooms = Room.objects.filter(tag=tag)

        if not tag:
            tag = u'所有'
        elif tag == 'music':
            tag = u'音乐'
        elif tag == 'sport':
            tag = u'体育'
        elif tag == 'game':
            tag = u'游戏'
        return render(request, self.template_name,
                {'tag':tag, 'rooms':rooms})
