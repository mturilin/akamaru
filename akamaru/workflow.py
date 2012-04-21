from akamaru import get_backend_dict, settings_getattr, RESOLVE_FORM_KEY, LOGIN_OK_KEY, LOGIN_ERROR_KEY
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

__author__ = 'mturilin'


class LoginWorkflow(object):
    session = None

    def __init__(self, backend_name):
        self.backend_name = backend_name
        self.backend = get_backend_dict()[backend_name]

    def get_session(self):
        return self.session

    def authenticate(self, *args, **kwargs):
        request = kwargs['request']

        self.session = self.backend.get_session(**{self.backend_name: request})
        user = authenticate(**{self.backend_name: self.session})

        if user:
            login(request, user)
            return redirect(reverse(settings_getattr(LOGIN_OK_KEY)))

        resolve_user = settings_getattr(RESOLVE_FORM_KEY)

        if not resolve_user:
            return redirect(reverse(settings_getattr(LOGIN_ERROR_KEY)))

        return redirect(reverse(resolve_user))


    def create_user(self, request, username, first_name, last_name, email, password):
        user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        social_user = self.backend.create_social_user(user, self.session)
        social_user.user = user
        social_user.save()

        user = authenticate(**{self.backend_name: self.session})
        login(request, user)
        return user

    def associate_user(self, request, user):
        social_user = self.backend.create_social_user(user, self.session)
        social_user.save()

        return user

    def is_authenticated(self):
        return self.get_session()