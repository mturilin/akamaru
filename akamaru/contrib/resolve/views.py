from akamaru import get_workflow, login_ok_redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm

def resolve(request):
    def _extract(d, keys):
        return dict((k, d[k]) for k in keys if k in d)

    workflow = get_workflow(request)

    if not workflow.is_authenticated():
        return redirect("/")

    if request.user.is_authenticated():
        workflow.associate_user(request, request.user)
        return login_ok_redirect()

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
            login(request, user)
            return login_ok_redirect()
    
    else:
        request.session.set_test_cookie()

    return render(request, "resolve/resolve.html", dict(create_user_form=create_user_form, login_form=login_form))