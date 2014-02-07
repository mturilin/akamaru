# -*- coding: utf-8 -*-
__author__ = 'mturilin'

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from oauthlib.oauth1 import Client
from oauthlib.oauth1.rfc5849 import SIGNATURE_TYPE_QUERY

from akamaru.models import SocialUser
from django.contrib.auth.models import User

import requests
import urlparse
import urllib


User = get_user_model()

LOGIN_OK_KEY = "AKAMARU_LOGIN_OK"
LOGIN_ERROR_KEY = "AKAMARU_LOGIN_ERROR"
WORKFLOW_SESSION_KEY = "AKAMARU_WORKFLOW"
RESOLVE_FORM_KEY = "AKAMARU_RESOLVE_FORM"
OAUTH_TOKEN_KEY = "AKAMARU_OAUTH_TOKEN"
OAUTH_TOKEN_SECRET_KEY = "AKAMARU_OAUTH_TOKEN_SECRET"


class AkamaruError(StandardError):
    pass


class BackendError(StandardError):
    pass


class AkamaruSession(object):
    def get_api_url(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")

    def me(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def is_token_expired(self):
        raise NotImplementedError("Subclasses must implement this method.")


class AkamaruBackend(object):
    def get_client_key(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_client_secret(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_login_url(self, request):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_backend_name(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def authenticate(self, **kwargs):
        if self.get_backend_name() in kwargs:
            session = kwargs[self.get_backend_name()]
            user = session.me()

            try:
                query = SocialUser.objects.get(backend=self.get_backend_name(), external_user_id=user['id'])
            except SocialUser.DoesNotExist:
                return None
            else:
                return query.user

    def create_social_user(self, user, session):
        social_user = SocialUser(user=user, external_user_id=session.me()['id'])
        social_user.save()
        social_user.backend = self.get_backend_name()
        return social_user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_redirect_url(self, request):
        return request.build_absolute_uri(get_callback_url(self.get_backend_name()))


class AkamaruOAuth1Backend(AkamaruBackend):
    def get_request_token_uri(self):
        raise NotImplementedError("Subclasses must implement this method.")    

    def get_authorize_token_uri(self):
        raise NotImplementedError("Subclasses must implement this method.")    

    def get_access_token_uri(self):
        raise NotImplementedError("Subclasses must implement this method.") 

    def _get_session(self):
        raise NotImplementedError("Subclasses must implement this method.") 

    def get_login_url(self, request):
        client = Client(client_key = unicode(self.get_client_key()), 
            client_secret = unicode(self.get_client_secret()), 
            resource_owner_key = u'', 
            resource_owner_secret = u'',
            callback_uri = unicode(self.get_redirect_url(request)),
            signature_type = SIGNATURE_TYPE_QUERY)

        token_url, _token_body, _token_headers = client.sign(unicode(self.get_request_token_uri()))

        res = requests.get(token_url)
        res_data = urlparse.parse_qs(res.text)

        if 'oauth_token' not in res_data:
            raise BackendError("Oauth provider didn't return access_token. %s" % res.text)

        request.session[OAUTH_TOKEN_SECRET_KEY] = res_data['oauth_token_secret'][0]

        authorization_url = self.get_authorize_token_uri()
        authorization_params = {'oauth_token': res_data['oauth_token'][0], 'oauth_callback': self.get_redirect_url(request)}

        url_parts = list(urlparse.urlparse(authorization_url))

        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(authorization_params)

        url_parts[4] = urllib.urlencode(query)

        return urlparse.urlunparse(url_parts)

    def get_session(self, **kwargs):
        if self.get_backend_name() in kwargs:
            auth_obj = kwargs[self.get_backend_name()]
            request = auth_obj

            if 'oauth_token' not in request.REQUEST:
                raise BackendError("Oauth provider didn't return access_token")

            oauth_token = request.REQUEST.get('oauth_token')
            oauth_verifier = request.REQUEST.get('oauth_verifier')

            client = Client(client_key = unicode(self.get_client_key()), 
                client_secret = unicode(self.get_client_secret()), 
                resource_owner_key = unicode(oauth_token), 
                resource_owner_secret = unicode(request.session[OAUTH_TOKEN_SECRET_KEY]),
                verifier = unicode(oauth_verifier),
                signature_type = SIGNATURE_TYPE_QUERY)

            access_url, _access_body, _access_header = client.sign(unicode(self.get_access_token_uri()))

            res = requests.get(access_url)
            res_data = urlparse.parse_qs(res.text)

            if 'oauth_token' not in res_data:
                raise BackendError("Oauth provider didn't return access_token. %s" % res.text)

            access_tokens = {
                'oauth_token_secret': res_data['oauth_token_secret'][0],
                'oauth_token': res_data['oauth_token'][0]
            }

            return self._get_session(**access_tokens)


def settings_getattr(key):
    val = getattr(settings, key, False)
    if not val:
        raise AkamaruError('%s was not found in settings' % key)
    return val

_backend_dict = None


def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def get_backend_dict():
    global _backend_dict

    if not _backend_dict:
        backend_str_list = getattr(settings, "AUTHENTICATION_BACKENDS")
        backend_class_list = [get_class(class_name) for class_name in backend_str_list]
        backend_list = [a_class() for a_class in backend_class_list if issubclass(a_class, AkamaruBackend)]
        _backend_dict = dict((backend.get_backend_name(), backend) for backend in backend_list)

    return _backend_dict


def get_workflow(request):
    if WORKFLOW_SESSION_KEY not in request.session:
        raise AkamaruError("Session middleware is not set up")
    workflow = request.session[WORKFLOW_SESSION_KEY]
    return workflow


def set_workflow(request, workflow):
    request.session[WORKFLOW_SESSION_KEY] = workflow


def login_ok_redirect():
    return redirect(reverse(settings_getattr(LOGIN_OK_KEY)))


def get_callback_url(backend_name):
    return reverse("akamaru-callback", args=(backend_name,))

