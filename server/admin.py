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

from server.models import Plotter, PlotConfig


class PlotterAdmin(admin.ModelAdmin):
    list_display = ('server_number', 'server_name', 'api_host', 'plotter_action')
    ordering = ('server_number',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['config', 'gateway', 'md5', 'version']

    def plotter_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">Restart Hpool</a>&nbsp;'
            '<a class="button" href="{}">Update Nagios</a>&nbsp;',
            reverse('admin:restart-hpool', args=[obj.pk]),
            reverse('admin:update-nagios', args=[obj.pk]),
        )

    plotter_action.allow_tags = True
    plotter_action.short_description = "Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(PlotterAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<server_id>.+)/restart-hpool/$',
                self.admin_site.admin_view(self.restart_hpool),
                name='restart-hpool',
            ),
            url(
                r'^(?P<server_id>.+)/update-nagios/$',
                self.admin_site.admin_view(self.update_nagios_config),
                name='update-nagios',
            ),
        ]

        return my_urls + urls


    def restart_hpool(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        api = PlotterAPI(plotter)
        result = api.restart_service('srv.hpool')
        messages.info(request, result['msg'])
        return HttpResponseRedirect(previous_url)

    def update_nagios_config(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        plotter = Plotter.objects.get(id=server_id)
        result = subprocess.check_call(["/opt/chia.website/deploy/scripts/config_nagios.sh",'%s' % plotter.server_number])
        messages.info(request, 'update plotter nagios config %s' % ( 'success' if result ==0 else 'fail') )
        return HttpResponseRedirect(previous_url)


class PlotConfigrAdmin(admin.ModelAdmin):
    list_display = ('name', 'k', 'e', 'n_threads', 'n_buckets', 'job_buffer', 'global_max_jobs', 'global_stagger_m',
                    'tmpdir_max_jobs', 'tmpdir_stagger_phase_major', 'tmpdir_stagger_phase_minor', 'tmpdir_stagger_phase_limit')

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                "fields": [
                    'name', 'description'
                ]
            }),
            ("Plotting", {
                'fields': [
                    'k', 'e', 'n_threads', 'n_buckets', 'job_buffer'
                ]
            }),

            ("Scheduling", {
                'fields': [
                    'tmpdir_stagger_phase_major', 'tmpdir_stagger_phase_minor', 'tmpdir_stagger_phase_limit',
                    'tmpdir_max_jobs', 'global_max_jobs', 'global_stagger_m'
                ]
            }),
        )

admin.site.register(Plotter, PlotterAdmin)
admin.site.register(PlotConfig, PlotConfigrAdmin)