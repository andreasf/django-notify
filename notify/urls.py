from django.conf.urls.defaults import *

urlpatterns = patterns('notify.views',
    (r'^challenge/(?P<username>.+)$', 'make_challenge', {}, "make_challenge"),
    (r'^(?P<challenge>.+)$', 'notify', {}, "notify"),
)
