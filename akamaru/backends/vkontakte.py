import json
import urlparse
from akamaru import AkamaruBackend, BackendError
from akamaru.models import SocialUser
from akamaru.app_settings import VKONTAKTE_APP_ID, VKONTAKTE_SECRET

from django.conf import settings
from django.contrib.auth.models import User
import requests

__author__ = 'pkorzh'

class VkontakteBackend(AkamaruBackend):
    def get_backend_name(self):
        return 'vkontakte'

    def create_social_user(self, user, session):
        social_user = SocialUser(user=user, external_user_id=session.me()['id'])
        social_user.save()
        social_user.backend = self.get_backend_name()
        return social_user

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

    def authenticate(self, **kwargs):
        if self.get_backend_name() in kwargs:
            vk_session = kwargs[self.get_backend_name()]
            vk_user = vk_session.me()

            try:
                query = SocialUser.objects.get(backend=self.get_backend_name(), external_user_id=vk_user['id'])
            except SocialUser.DoesNotExist:
                return None
            else:
                return query.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    def get_login_url(self, request):
        return "http://api.vk.com/oauth/authorize?client_id=%s&redirect_uri=%s" % (
            VKONTAKTE_APP_ID, self.get_redirect_url(request))


    def get_authorize_url(self, request, code):
        return "https://api.vk.com/oauth/token?client_id=%s&code=%s&client_secret=%s" %\
               (VKONTAKTE_APP_ID, code, VKONTAKTE_SECRET)


class VkontakteSession(object):
    URL_USER = "https://api.vk.com/method/users.get"

    def __init__(self, access_token, user_id): 
        self.access_token = access_token
        self.user_id = user_id

    def vk_api(self, url, user_id):
        resp = json.loads(requests.get(url, params={"access_token": self.access_token, "uids": user_id}).text)

        if 'response' in resp:
            resp = resp['response'][0]
        else:
            raise BackendError("Vkontakte session error.")

        resp.update({
            'id': resp['uid']
        })

        return resp

    def user(self, user_id):
        return self.vk_api(VkontakteSession.URL_USER, user_id)

    def me(self):
        return self.user(self.user_id)



