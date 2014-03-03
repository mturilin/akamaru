# -*- coding: utf-8 -*-
__author__ = 'gusevsergey'

from django.contrib import admin
from .models import SocialUser


class SocialUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'backend')

admin.site.register(SocialUser, SocialUserAdmin)