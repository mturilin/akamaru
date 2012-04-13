from akamaru import get_backend_dict, AkamaruError, get_workflow, set_workflow, login_ok_redirect
from akamaru.workflow import LoginWorkflow
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate

from akamaru.forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm

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

def resolve(request):
    def _extract(d, keys):
        return dict((k, d[k]) for k in keys if k in d)

    workflow = get_workflow(request)

    if not workflow.is_authenticated():
        return redirect("/")

    create_user_form = CreateUserForm(request.POST or None, initial = workflow.get_session().me())
    login_form = AuthenticationForm(request, request.POST or None)

    if create_user_form.is_valid():
        workflow.create_user(
            request,
            **(_extract(create_user_form.cleaned_data, [
                'username',
                'password',
                'first_name',
                'last_name',
                'email'])))
        return login_ok_redirect()
    
    elif login_form.is_valid():
        user = authenticate(username = login_form.cleaned_data['username'], password = login_form.cleaned_data['password'])
        if user and user.is_active:
            workflow.associate_user(request, user)
            return login_ok_redirect()
    
    else:
        request.session.set_test_cookie()

    return render(request, "resolve.html", dict(create_user_form=create_user_form, login_form=login_form))