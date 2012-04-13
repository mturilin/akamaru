import json
import urlparse
from akamaru import AkamaruBackend, BackendError
from akamaru.models import SocialUser
from akamaru.app_settings import FACEBOOK_APP_ID, FACEBOOK_SECRET

from django.conf import settings
from django.contrib.auth.models import User
import requests

__author__ = 'mturilin'

class FacebookBackend(AkamaruBackend):
    def get_backend_name(self):
        return 'facebook'

    def create_social_user(self, user, session):
        social_user = SocialUser(user=user, external_user_id=session.me()['id'])
        social_user.save()
        social_user.backend = self.get_backend_name()
        return social_user

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

            access_token = res_data['access_token']
            fb_session = FacebookSession(access_token)

        return fb_session

    def authenticate(self, **kwargs):
        if self.get_backend_name() in kwargs:
            fb_session = kwargs[self.get_backend_name()]
            fb_user = fb_session.me()

            try:
                query = SocialUser.objects.get(backend=self.get_backend_name(), external_user_id=fb_user['id'])
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
        return "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s" % (
            self.get_app_id(), self.get_redirect_url(request))


    def get_authorize_url(self, request, code):
        return "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" %\
               (FACEBOOK_APP_ID, self.get_redirect_url(request), FACEBOOK_SECRET, code)


class FacebookSession(object):
    URL_USER = "https://graph.facebook.com/"

    def __init__(self, access_token): self.access_token = access_token

    def open_graph(self, url):
        return json.loads(requests.get(url, params={"access_token": self.access_token}).text)

    def user(self, username):
        return self.open_graph(FacebookSession.URL_USER + username)

    def me(self):
        return self.user("me")



