from views import *
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^show/(?P<tag>.*?)/?$', ShowView.as_view(), name='show'),
    url(r'^/?$', HomeView.as_view(), name='home'),
    # Examples:
    # url(r'^$', 'live_portal.views.home', name='home'),
    # url(r'^live_portal/', include('live_portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
