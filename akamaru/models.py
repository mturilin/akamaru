# -*- coding: utf-8 -*-
__author__ = 'mturilin'

from django.db import models
from django.contrib.auth import get_user_model


class SocialUser(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='social_users')
    external_user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    backend = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s; %s" % (self.backend, self.user)