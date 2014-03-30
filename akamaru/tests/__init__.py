__author__ = 'gusevsergey'

from django.test import TestCase
from django.conf import settings
from .backends import *
from .workflow import *
from akamaru import LOGIN_ERROR_KEY


class SettingsTest(TestCase):
    def test_error_url(self):
        self.assertTrue(getattr(settings, LOGIN_ERROR_KEY, False))