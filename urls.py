from akamaru_demo.views import index, profile, resolve
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^profile/$', profile, name='profile'),
    url(r'^akamaru/', include('akamaru.urls')),
)



