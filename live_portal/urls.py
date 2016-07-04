from views import *
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from registration.backends.simple.views import RegistrationView

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon/1.ico')),

    # auth & accounts
    url(r'^auth', TemplateView.as_view(template_name='registration/auth.html'), name='auth'),
    url(r'^accounts/register/$',
              RegistrationView.as_view(form_class=CrikeRegistrationForm),
              name='registration_register'),

    # follows
    url(r'^user/follows$', login_required(UserFollowsView.as_view()), name='user_follows'),

    # show anchors
    url(r'^show/(?P<tag>.*?)/?$', ShowView.as_view(), name='show'),
    url(r'^/?$', HomeView.as_view(), name='home'),
)
