from akamaru.views import start_login, callback
from django.conf.urls.defaults import url, patterns

__author__ = 'mturilin'


urlpatterns = patterns('',
    url(r'^complete/(?P<backend_name>[^/]+)/$', callback, name='akamaru-callback'),
    url(r'^login/(?P<backend_name>[^/]+)/$', start_login, name='akamaru-login'),
)


