import json
import urlparse
from akamaru import AkamaruOAuth1Backend, AkamaruSession, BackendError, settings_getattr
from akamaru.models import SocialUser

from django.conf import settings
from django.contrib.auth.models import User
import requests

from django.conf import settings

__author__ = 'pkorzh'

class TrelloBackend(AkamaruOAuth1Backend):
    def get_backend_name(self):
        return 'trello'

    def get_client_key(self):
        return settings_getattr('TRELLO_API_KEY')

    def get_client_secret(self):
        return settings_getattr('TRELLO_TOKEN')

    def get_request_token_uri(self):
        return 'https://trello.com/1/OAuthGetRequestToken'   

    def get_authorize_token_uri(self):
        return 'https://trello.com/1/OAuthAuthorizeToken'

    def get_access_token_uri(self):
        return 'https://trello.com/1/OAuthGetAccessToken'  

    def _get_session(self, oauth_token, oauth_token_secret):
        return TrelloSession(oauth_token, oauth_token_secret, self.get_client_key())


class TrelloSession(AkamaruSession):
    def __init__(self, oauth_token, oauth_token_secret, client_key):
        self.oauth_token_secret = oauth_token_secret
        self.oauth_token = oauth_token
        self.client_key = client_key

    def me(self):
        res = requests.get(u'https://api.trello.com/1/members/me?token=%s&key=%s' % (self.oauth_token, self.client_key))
        res_data = json.loads(res.text)

        return res_data

    def is_token_expired(self):
        return False

