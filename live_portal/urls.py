from views import *
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from registration.backends.simple.views import RegistrationView
from forms import *

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon/1.ico')),

    # auth & accounts
    url(r'^auth', TemplateView.as_view(template_name='registration/auth.html'), name='auth'),
    url(r'^accounts/register/$',
              RegistrationView.as_view(form_class=LivePortalRegistrationForm),
              name='registration_register'),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset', name='auth_password_reset'),
    url(r'^changepassword/passwordsent/$', 'django.contrib.auth.views.password_change', name='auth_password_change'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='auth_logout'),

    # follows
    url(r'^user/follows$', login_required(UserFollowsView.as_view()), name='user_follows'),

    # show anchors
    url(r'^show/(?P<tag>.*?)/?$', ShowView.as_view(), name='show'),
    url(r'^/?$', HomeView.as_view(), name='home'),
)
