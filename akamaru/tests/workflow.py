# -*- coding: utf-8 -*-

from django.test import TestCase
from akamaru import settings_getattr, LOGIN_ERROR_KEY, PermissionDeniedException
from akamaru.workflow import LoginWorkflow
from django.core.urlresolvers import reverse
from mock import patch


__author__ = 'gusevsergey'


class WorkFlowTest(TestCase):
    def test_permission_denied(self):
        u"""
        Если при попытке получить объект сессии возникает исключение PermissionDenied,
        то делаем редирект на страницу ошибки. """
        workflow = LoginWorkflow('facebook')
        with patch.object(workflow, 'backend') as mock:
            mock.configure_mock(**{
                'get_session.side_effect': PermissionDeniedException
            })
            result = workflow.authenticate(**{'request': None})
            self.assertEquals(result['Location'],
                              reverse(settings_getattr(LOGIN_ERROR_KEY))+'?error=permission%20denied')
