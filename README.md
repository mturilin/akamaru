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
- Vkontakte

Usage
------------------
settings.py:

    AUTHENTICATION_BACKENDS = (
        ...
        'akamaru.backends.facebook.FacebookBackend',
        'akamaru.backends.vkontakte.VkontakteBackend',
        ...
        'django.contrib.auth.backends.ModelBackend',
    )

    INSTALLED_APPS = (
        ...
        'akamaru',
    )

urls.py:

    urlpatterns = patterns('',
        ...
        url(r'', include('akamaru.urls')),
    )

run syncdb

Configuration
------------------
Setup needed OAuth keys in your settings.py:

    FACEBOOK_APP_ID = ""
    FACEBOOK_SECRET = ""
    VKONTAKTE_APP_ID = '2806299'
    VKONTAKTE_SECRET = '30euNDsQIJTY1FP3fQrb'

Setup urls.py names:

    AKAMARU_LOGIN_OK = "profile"
    AKAMARU_LOGIN_ERROR = "login-error"
    AKAMARU_RESOLVE_FORM = "create_user"