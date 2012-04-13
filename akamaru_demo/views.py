from akamaru import get_workflow, login_ok_redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

__author__ = 'mturilin'


def index(request):
    return render(request, "index.html")

@login_required
def profile(request):
    return render(request, "profile.html", {'user': request.user })