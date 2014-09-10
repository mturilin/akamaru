# -*- coding: utf-8 -*-
__author__ = 'mturilin'

from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateUserForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is not unique")

        return username