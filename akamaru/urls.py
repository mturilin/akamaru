from akamaru.views import start_login, callback
from akamaru.contrib.resolve.views import resolve
from django.conf.urls.defaults import url, patterns

__author__ = 'mturilin'

urlpatterns = patterns('',
    url(r'^complete/(?P<backend_name>[^/]+)/$', callback, name='akamaru-callback'),
    url(r'^login/(?P<backend_name>[^/]+)/$', start_login, name='akamaru-login'),
    url(r'^resolve/$', resolve, name='akamaru-resolve'),
)