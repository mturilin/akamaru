# -*- coding: utf-8 -*-
__author__ = 'pkorzh'

import json
import requests
from akamaru import AkamaruOAuth1Backend, AkamaruSession, settings_getattr, BackendError
from django.conf import settings

GOOGLE_CONSUMER_KEY_KEY = 'GOOGLE_CONSUMER_KEY'
GOOGLE_CONSUMER_SECRET_KEY = 'GOOGLE_CONSUMER_SECRET'
GOOGLE_SCOPE = 'GOOGLE_SCOPE'


class GoogleBackend(AkamaruOAuth1Backend):
    class AccessDeniedException(Exception):
        pass

    def get_backend_name(self):
        return 'google'

    def get_client_key(self):
        return settings_getattr(GOOGLE_CONSUMER_KEY_KEY)

    def get_client_secret(self):
        return settings_getattr(GOOGLE_CONSUMER_SECRET_KEY)

    def get_request_token_uri(self):
        return 'https://www.google.com/accounts/OAuthGetRequestToken?scope=https://www.googleapis.com/auth/plus.me'

    def get_authorize_token_uri(self):
        return 'https://www.google.com/accounts/OAuthAuthorizeToken'

    def get_access_token_uri(self):
        return 'https://www.google.com/accounts/OAuthGetAccessToken'  

    def _get_session(self, oauth_token, oauth_token_secret):
        return GoogleSession(oauth_token, oauth_token_secret, self.get_client_key(), self.get_client_secret())

    def get_login_url(self, request):
        return "https://accounts.google.com/o/oauth2/auth?" + \
            "redirect_uri=%s" % self.get_redirect_url(request) + \
            "&response_type=code" + \
            "&client_id=%s" % getattr(settings, GOOGLE_CONSUMER_KEY_KEY, '') + \
            "&scope=%s" % getattr(settings, GOOGLE_SCOPE, '')

    def get_authorize_url(self):
        return

    def get_session(self, **kwargs):
        google_session = None

        if not self.get_backend_name() in kwargs:
            return google_session

        auth_obj = kwargs[self.get_backend_name()]

        # auth obj could be session or request
        if isinstance(auth_obj, GoogleSession):
            return auth_obj

        request = auth_obj
        if 'error' in request.REQUEST and request.REQUEST['error'] == 'access_denied':
            raise self.AccessDeniedException()

        if 'code' not in request.REQUEST:
            raise BackendError('Google data doesn\'t have "code"')

        code = request.REQUEST.get('code')

        request_result = requests.post(
            u"https://accounts.google.com/o/oauth2/token",
            data={
                'code': code,
                'client_id': getattr(settings, GOOGLE_CONSUMER_KEY_KEY, ''),
                'client_secret': getattr(settings, GOOGLE_CONSUMER_SECRET_KEY, ''),
                'redirect_uri': self.get_redirect_url(request),
                'grant_type': 'authorization_code'
            },
            headers={'content-type': 'application/x-www-form-urlencoded'})
        res_data = json.loads(request_result.text.strip())

        if 'access_token' not in res_data:
            raise BackendError("Google didn't return access_token. Response: %s" % request_result.text)
        access_token = res_data['access_token']

        google_session = GoogleSession(access_token)
        print google_session.me()

        return google_session


class GoogleSession(AkamaruSession):
    def __init__(self, access_token):
        self.access_token = access_token

    def me(self):
        d = requests.get(u"https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s" % (self.access_token,))
        return json.loads(d.text.strip())

