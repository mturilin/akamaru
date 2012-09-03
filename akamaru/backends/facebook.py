import json
import urlparse
from urllib import urlencode

from akamaru import AkamaruBackend, AkamaruSession, BackendError, settings_getattr
from akamaru.models import SocialUser

from django.conf import settings
from django.contrib.auth.models import User
import requests

__author__ = 'mturilin'

FACEBOOK_APP_ID_KEY = 'FACEBOOK_APP_ID'
FACEBOOK_SECRET_KEY = 'FACEBOOK_SECRET'

class FacebookBackend(AkamaruBackend):
    def get_backend_name(self):
        return 'facebook'

    def get_client_key(self):
        return settings_getattr(FACEBOOK_APP_ID_KEY)

    def get_client_secret(self):
        return settings_getattr(FACEBOOK_SECRET_KEY)

    def get_session(self, **kwargs):
        fb_session = None
        if self.get_backend_name() in kwargs:
            auth_obj = kwargs[self.get_backend_name()]

            # auth obj could be session or request
            if isinstance(auth_obj, FacebookSession):
                return auth_obj

            request = auth_obj
            if 'code' not in request.REQUEST:
                raise BackendError('Facebook data doesn\'t have "code"')

            code = request.REQUEST['code']

            request_result = requests.get(self.get_authorize_url(request, code))
            res_data = urlparse.parse_qs(request_result.text.strip())

            if 'access_token' not in res_data:
                raise BackendError("Facebook didn't return access_token. Response: %s" % request_result.text)

            access_token = res_data['access_token'][0]
            fb_session = FacebookSession(access_token)

        return fb_session

    def get_login_url(self, request):
        return "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s" % (
            self.get_client_key(), self.get_redirect_url(request))


    def get_authorize_url(self, request, code):
        return "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" %\
               (self.get_client_key(), self.get_redirect_url(request), self.get_client_secret(), code)


class FacebookSession(AkamaruSession):
    def __init__(self, access_token): 
        self.access_token = access_token

    def get_api_url(self, fb_username, *args, **kwargs):
        kwargs.update({'access_token': self.access_token})

        url = "https://graph.facebook.com/%s" % fb_username

        if kwargs:
            url += "?" + urlencode(kwargs)

        return url

    def me(self):
        url = self.get_api_url('me')
        me = json.loads(requests.get(url).text)

        if 'location' in me.keys():
            location_parts = me['location']['name'].split(', ')
            if len(location_parts) >= 2:
                me['city'] = location_parts[0]
                me['country'] = location_parts[1]
            else:
                me['city'] = me.location
                me['country'] = ''
        else:
            me['city'] = ''
            me['country'] = ''

        return me

    def getFriends(self):
        url = self.get_api_url('me/friends')
        resp = json.loads(requests.get(url).text)

        if 'data' in resp:
            friends = resp['data']

            def map_name(friend):
                name_parts = friend['name'].split(' ')

                if len(name_parts) >= 2:
                    friend['first_name'] = name_parts[0]
                    friend['last_name'] = name_parts[1]
                else:
                    friend['first_name'] = friend.name
                    friend['last_name'] = ''

                return friend

            return map(map_name, friends)

        return []

    def is_token_expired(self):
        """
            http://developers.facebook.com/blog/post/2011/05/13/how-to--handle-expired-access-tokens/
        """
        url = self.get_api_url('me')
        data = json.loads(requests.get(url).text)
        
        if 'error' in data:
            return 'OAuthException' == data['error'].get('type', '')

        return False


