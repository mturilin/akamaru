# -*- coding: utf-8 -*-
from akamaru.contrib.resolve.views import resolve
from django.conf.urls import url, patterns

__author__ = 'mturilin'

urlpatterns = patterns('akamaru.views',
    url(r'^complete/(?P<backend_name>[^/]+)/$', 'callback', name='akamaru-callback'),
    url(r'^login/(?P<backend_name>[^/]+)/$', 'start_login', name='akamaru-login'),
    url(r'^resolve/$', resolve, name='akamaru-resolve'),
    url(r'^shut_off/(?P<backend_name>[^/]+)/$', 'shut_off', name='akamaru-shut-off')
)