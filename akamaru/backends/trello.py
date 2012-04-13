import json
import urlparse
from akamaru import AkamaruBackend, BackendError
from akamaru.models import SocialUser

from django.conf import settings
from django.contrib.auth.models import User
import requests

__author__ = 'pkorzh'

class TrelloBackend(AkamaruBackend):
    OAuthGetRequestToken = 'https://trello.com/1/OAuthGetRequestToken'
    OAuthAuthorizeToken = 'https://trello.com/1/OAuthAuthorizeToken'
    OAuthGetAccessToken = 'https://trello.com/1/OAuthGetAccessToken'

    def get_backend_name(self):
        return 'trello'

    def create_social_user(self, user, session):
        social_user = SocialUser(user=user, external_user_id=session.me()['id'])
        social_user.save()
        social_user.backend = self.get_backend_name()
        return social_user

    def get_session(self, **kwargs):
        pass

    def authenticate(self, **kwargs):
        if self.get_backend_name() in kwargs:
            t_session = kwargs[self.get_backend_name()]
            t_user = t_session.me()

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
        return ''


    def get_authorize_url(self, request, code):
        return ''


class TrelloSession(object):
    pass



