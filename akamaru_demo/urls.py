from demo.views import index, profile
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^profile/$', profile, name='profile'),
    url(r'^akamaru/', include('akamaru.urls')),
)



