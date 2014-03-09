# -*- coding: utf-8 -*-
__author__ = 'gusevsergey'

from django.test import TestCase
from django.test.client import RequestFactory
from akamaru.backends.facebook import FacebookBackend


class FacebookBackendTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.backend = FacebookBackend()

    def test_get_session_access_denied(self):
        with self.assertRaises(FacebookBackend.AccessDeniedException):
            self.backend.get_session(
                facebook=self.factory.get('/', data={'error': 'access_denied'}))
