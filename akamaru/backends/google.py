# -*- coding: utf-8 -*-
__author__ = 'pkorzh'

import json
import requests
from akamaru import AkamaruOAuth1Backend, AkamaruSession, settings_getattr
from oauthlib.oauth1 import Client
from oauthlib.oauth1.rfc5849 import SIGNATURE_TYPE_QUERY


GOOGLE_CONSUMER_KEY_KEY = 'GOOGLE_CONSUMER_KEY'
GOOGLE_CONSUMER_SECRET_KEY = 'GOOGLE_CONSUMER_SECRET'


class GoogleBackend(AkamaruOAuth1Backend):
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


class GoogleSession(AkamaruSession):
    def __init__(self, oauth_token, oauth_token_secret, client_key, client_secret):
        self.oauth_token_secret = oauth_token_secret
        self.oauth_token = oauth_token
        self.client_key = client_key
        self.client_secret = client_secret

    def me(self):
        client = Client(client_key = unicode(self.client_key), 
            client_secret = unicode(self.client_secret), 
            resource_owner_key = unicode(self.oauth_token), 
            resource_owner_secret = unicode(self.oauth_token_secret),
            signature_type = SIGNATURE_TYPE_QUERY)

        url = client.sign(unicode('https://www.googleapis.com/oauth2/v1/userinfo?alt=json'))[0]
        
        res = json.loads(requests.get(url).text)
        res.update({'first_name': res.get('given_name'), 'last_name': res.get('family_name')})

        return res

    def is_token_expired(self):
        return False
