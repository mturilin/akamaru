import json
import urlparse
from urllib import urlencode

from akamaru import AkamaruBackend, AkamaruSession, BackendError, settings_getattr
from akamaru.models import SocialUser

from django.conf import settings
from django.contrib.auth.models import User
import requests

__author__ = 'pkorzh'

VKONTAKTE_APP_ID_KEY = 'VKONTAKTE_APP_ID'
VKONTAKTE_SECRET_KEY = 'VKONTAKTE_SECRET'

class VkontakteBackend(AkamaruBackend):
    def get_backend_name(self):
        return 'vkontakte'

    def get_client_key(self):
        return settings_getattr(VKONTAKTE_APP_ID_KEY)

    def get_client_secret(self):
        return settings_getattr(VKONTAKTE_SECRET_KEY)

    def get_session(self, **kwargs):
        vk_session = None
        if self.get_backend_name() in kwargs:
            auth_obj = kwargs[self.get_backend_name()]

            # auth obj could be session or request
            if isinstance(auth_obj, VkontakteSession):
                return auth_obj

            request = auth_obj
            if 'code' not in request.REQUEST:
                raise BackendError('Vkontakte data doesn\'t have "code"')

            code = request.REQUEST.get('code')

            request_result = requests.get(self.get_authorize_url(request, code))
            res_data = json.loads(request_result.text.strip())

            if 'access_token' not in res_data:
                raise BackendError("Vkontakte didn't return access_token. Response: %s" % request_result.text)

            access_token = res_data['access_token']
            user_id = res_data['user_id']
            vk_session = VkontakteSession(access_token, user_id)

        return vk_session


    def get_login_url(self, request):
        return "http://api.vk.com/oauth/authorize?client_id=%s&redirect_uri=%s" % (
            self.get_client_key(), self.get_redirect_url(request))


    def get_authorize_url(self, request, code):
        return "https://api.vk.com/oauth/token?client_id=%s&code=%s&client_secret=%s" %\
               (self.get_client_key(), code, self.get_client_secret())


class VkontakteSession(AkamaruSession):
    def __init__(self, access_token, user_id): 
        self.access_token = access_token
        self.user_id = user_id

    def get_api_url(self, vk_method, *args, **kwargs):
        kwargs.update({'access_token': self.access_token})

        url = "https://api.vk.com/method/%s" % vk_method

        if kwargs:
            url += "?" + urlencode(kwargs)

        return url

    def me(self):
        url = self.get_api_url('users.get', **{"uids": self.user_id})

        resp = json.loads(requests.get(url).text)
        profile = resp['response'][0]
        profile.update({'id': profile['uid']})

        return profile



