from django.contrib.auth.models import User

__author__ = 'mturilin'

from django.db import models

class SocialUser(models.Model):
    user = models.ForeignKey(User, related_name='social_users')
    external_user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    backend = models.CharField(max_length=255)
