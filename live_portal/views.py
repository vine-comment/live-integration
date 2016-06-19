#coding:utf-8

import MySQLdb

from django.views.generic import *
from django.http import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from live_portal.models import *

class ShowAllView(TemplateView):
    template_name = 'live_portal_showall.html'
    ''' 
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='Intel132',port=3306)
        cur=conn.cursor()
        conn.select_db('live_portal')
        count=cur.execute('select * from live_portal')
        print 'there has %s rows record' % count
     
        result=cur.fetchone()
        print result
        print 'ID: %s info %s' % result
     
        results=cur.fetchmany(5)
        for r in results:
            print r
     
        print '=='*10
        cur.scroll(0,mode='absolute')
     
        results=cur.fetchall()
        for r in results:
            print r[1]
         
        conn.commit()
        cur.close()
        conn.close()
         
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    '''
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        return render(request, self.template_name, {'rooms':rooms})
