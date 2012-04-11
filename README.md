Akamaru
==================
Very simple social auth backend for Django 

Requirements
------------------
- path.py
- requests

Supported auth backends
------------------
- Facebook

Usage
------------------
settings.py:

    AUTHENTICATION_BACKENDS = (
        ...
        'akamaru.backends.facebook.FacebookBackend',
        ...
        'django.contrib.auth.backends.ModelBackend',
    )

urls.py:

    urlpatterns = patterns('',
        ...
        url(r'', include('akamaru.urls')),
    )

