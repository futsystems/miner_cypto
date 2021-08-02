# -*- coding: utf-8 -*-


from django.contrib import admin

# Register your models here.

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.helpers import ActionForm
from django.contrib import admin,messages
from django.db import connection
from django.utils.html import format_html
from django import forms
from django.shortcuts import render_to_response
from django.db.models import Max
from collections import OrderedDict
import subprocess
import logging,traceback,json
logger = logging.getLogger(__name__)

from .models import Game

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'url')

admin.site.register(Game, GameAdmin)

