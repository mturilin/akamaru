from akamaru_demo.views import index, profile, resolve
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^login/$', resolve, name='create_user'),
    url(r'^profile/$', profile, name='profile'),
    url(r'', include('akamaru.urls')),
)



