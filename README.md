Akamaru
==================
Very simple social auth backend for Django 

Requirements
------------------
- django
- path.py
- requests
- oauthlib

Supported auth backends
------------------
- Facebook
- Vkontakte
- Google
- Trello

Usage
------------------
settings.py:

    AUTHENTICATION_BACKENDS = (
        ...
        'akamaru.backends.facebook.FacebookBackend',
        'akamaru.backends.vkontakte.VkontakteBackend',
        'akamaru.backends.google.GoogleBackend',
        'akamaru.backends.trello.TrelloBackend',
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

    FACEBOOK_APP_ID = ''
    FACEBOOK_SECRET = ''

    VKONTAKTE_APP_ID = ''
    VKONTAKTE_SECRET = ''

    TRELLO_API_KEY = ''
    TRELLO_TOKEN = ''

    GOOGLE_CONSUMER_KEY = ''
    GOOGLE_CONSUMER_SECRET = ''

Setup urls.py names:

    AKAMARU_LOGIN_OK = "profile"
    AKAMARU_LOGIN_ERROR = "login-error"
    AKAMARU_RESOLVE_FORM = "resolve"