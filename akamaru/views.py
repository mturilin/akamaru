from akamaru import get_backend_dict, get_workflow, set_workflow, login_ok_redirect
from akamaru.exceptions import AkamaruError
from akamaru.workflow import LoginWorkflow
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate

__author__ = 'mturilin'


def start_login(request, backend_name):
    set_workflow(request, LoginWorkflow(backend_name))
    return redirect(get_backend_dict()[backend_name].get_login_url(request))

def callback(request, backend_name):
    workflow = get_workflow(request)

    if workflow.backend_name != backend_name:
        raise AkamaruError("Workflow")

    request.session.modified = True

    return workflow.authenticate(**{'request': request})