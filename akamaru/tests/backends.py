# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import RequestFactory
from akamaru import PermissionDeniedException
from akamaru.backends.facebook import FacebookBackend
from akamaru.backends.vkontakte import VkontakteBackend
from akamaru.backends.google import GoogleBackend

__author__ = 'gusevsergey'


class FacebookBackendTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.backend = FacebookBackend()

    def test_get_session_access_denied(self):
        with self.assertRaises(PermissionDeniedException):
            self.backend.get_session(
                facebook=self.factory.get('/', data={'error': 'access_denied'}))


class VkontakteBackendTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.backend = VkontakteBackend()

    def test_get_session_access_denied(self):
        with self.assertRaises(PermissionDeniedException):
            self.backend.get_session(
                vkontakte=self.factory.get('/', data={'error': 'access_denied', 'error_reason': 'user_denied'}))


class GoogleBackendTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.backend = GoogleBackend()

    def test_get_session_access_denied(self):
        with self.assertRaises(PermissionDeniedException):
            self.backend.get_session(
                google=self.factory.get('/', data={'error': 'access_denied'}))
