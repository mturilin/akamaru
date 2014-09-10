# -*- coding: utf-8 -*-
__author__ = 'mturilin'

import traceback
import sys
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect
from akamaru import get_backend_dict, get_workflow, set_workflow, AkamaruError, settings_getattr
from akamaru.workflow import LoginWorkflow


AKAMARU_ILLEGAL_STATE_REDIRECT = "AKAMARU_ILLEGAL_STATE_REDIRECT"


def start_login(request, backend_name):
    set_workflow(request, LoginWorkflow(backend_name))
    return redirect(get_backend_dict()[backend_name].get_login_url(request))


def callback(request, backend_name):
    try:
        workflow = get_workflow(request)
        if workflow.backend_name != backend_name:
            raise AkamaruError("Workflow")
    except AkamaruError:
        traceback.print_exc(file=sys.stdout)
        if hasattr(settings, AKAMARU_ILLEGAL_STATE_REDIRECT):
            akamaru_illegal_state_redirect = settings_getattr(AKAMARU_ILLEGAL_STATE_REDIRECT)
            return HttpResponseRedirect(akamaru_illegal_state_redirect)
        return HttpResponseRedirect('/')

    request.session.modified = True
    return workflow.authenticate(**{'request': request})


def shut_off(request, backend_name):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    request.user.social_users.filter(backend=backend_name).delete()
    return HttpResponseRedirect(request.GET['success_url'])
