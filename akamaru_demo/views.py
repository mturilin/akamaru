from akamaru import get_workflow, login_ok_redirect
from akamaru_demo.forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

__author__ = 'mturilin'


def index(request):
    return render(request, "index.html")

def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)

def resolve(request):
    workflow = get_workflow(request)

    if not workflow.is_authenticated():
        print("Not authenticated")
        return redirect("/")

    if request.method == 'GET':
        create_user_form = CreateUserForm()
        login_form = AuthenticationForm()

    else:
        create_user_form = CreateUserForm(request.REQUEST)
        login_form = AuthenticationForm(request.REQUEST)

        if create_user_form.is_valid():
            workflow.create_user(
                request,
                **(extract(create_user_form.cleaned_data, [
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                    'email'])))
            return login_ok_redirect()




    return render(request, "resolve.html", dict(create_user_form=create_user_form, login_form=login_form))


@login_required
def profile(request):
    return render(request, "profile.html", {'user': request.user })