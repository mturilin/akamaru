# -*- coding: utf-8 -*-
from demo.views import index, profile
from django.conf.urls import patterns, url, include
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', index),
    url(r'^profile/$', profile, name='profile'),
    url(r'^akamaru/', include('akamaru.urls')),

    ## Django default stuff
    url(r'^admin/', include(admin.site.urls)),
)



