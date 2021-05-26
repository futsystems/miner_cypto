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

from server.models import Plotter, PlotConfig, Harvester, PlotTransfer


class PlotterAdmin(admin.ModelAdmin):
    list_display = ('server_number', 'cache_type', 'plot_config_content', 'output',
                    'time', 'statistic', 'cpu', 'mem', 'thread', 'is_cache_raid0', 'up_time', 'is_plotting_run', 'is_sending_run', 'plotter_action')
    ordering = ('server_number',)
    list_filter = ('cache_type',)
    search_fields = ('server_number', 'description')

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['server_number', 'plot_config_applied']

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                "fields": [
                    'server_number', 'cache_cnt', 'cache_type', 'is_cache_raid0', 'plot_config', 'exclude_plot_dst_path'
                ]
            }),

            ("Harvester", {
                'fields': [
                    'harvester'
                ]
            }),

            ("Others", {
                'fields': [
                    'is_plotting_run', 'boot_time', 'description'
                ]
            }),

            ("Info", {
                'fields': [
                    'internal_ip', 'is_sending_run'
                ]
            }),

            ("Hardware", {
                'fields': [
                    'cpu_model', 'cpu_cnt', 'cpu_used_percent', 'memory_total', 'memory_used',
                ]
            }),
        )

    def plotter_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">U</a>&nbsp;'
            '<a class="button" href="{}">T</a>&nbsp;'
            '<a class="button" href="{}">N</a>&nbsp;'
            '<a class="button" href="{}">H(R)</a>&nbsp;'
            '<a class="button" href="{}">P(R)</a>&nbsp;'
            '<a class="button" href="{}">StartSending</a>&nbsp;'
            '<a class="button" href="{}">StopSending</a>&nbsp;',
            reverse('admin:update-system', args=[obj.pk]),
            reverse('admin:pki-ticket', args=[obj.pk]),
            reverse('admin:update-nagios', args=[obj.pk]),
            reverse('admin:restart-hpool', args=[obj.pk]),
            reverse('admin:apply-plot-config', args=[obj.pk]),
            reverse('admin:plotter-start-sending', args=[obj.pk]),
            reverse('admin:plotter-stop-sending', args=[obj.pk]),
        )

    plotter_action.allow_tags = True
    plotter_action.short_description = "Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(PlotterAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<server_id>.+)/update-system/$',
                self.admin_site.admin_view(self.update_system),
                name='update-system',
            ),
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
            url(
                r'^(?P<server_id>.+)/pki-ticket/$',
                self.admin_site.admin_view(self.pki_ticket),
                name='pki-ticket',
            ),

            url(
                r'^(?P<server_id>.+)/apply-plot-config/$',
                self.admin_site.admin_view(self.apply_plot_config),
                name='apply-plot-config',
            ),

            url(
                r'^(?P<server_id>.+)/plotter-start-sending/$',
                self.admin_site.admin_view(self.start_sending),
                name='plotter-start-sending',
            ),

            url(
                r'^(?P<server_id>.+)/plotter-stop-sending/$',
                self.admin_site.admin_view(self.stop_sending),
                name='plotter-stop-sending',
            ),
        ]

        return my_urls + urls

    def update_system(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        api = PlotterAPI(plotter)
        result = api.update_system()
        messages.info(request, '%s %s' % (plotter.server_name(), result['msg']))
        return HttpResponseRedirect(previous_url)

    def restart_hpool(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        api = PlotterAPI(plotter)
        result = api.restart_service('srv.hpool')
        messages.info(request, '%s %s' % (plotter.server_name(), result['msg']))
        return HttpResponseRedirect(previous_url)

    def update_nagios_config(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        plotter = Plotter.objects.get(id=server_id)
        import requests
        query = {'id': plotter.server_number}
        response = requests.get('http://127.0.0.1:8080/icinga2/config/plotter', params=query)

        messages.info(request,  '%s %s' % (plotter.server_name(),response.content))
        #result = subprocess.check_call(["/opt/chia.website/deploy/scripts/config_nagios.sh",'%s' % plotter.server_number])
        #result = subprocess.check_output(["/etc/icinga2/zones.d/master/config_plotter.sh", "%s" % plotter.server_number])
        #messages.info(request, 'update plotter-%s nagios config %s' % (plotter.server_number,( 'success' if result ==0 else 'fail') ))
        return HttpResponseRedirect(previous_url)

    def pki_ticket(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        plotter = Plotter.objects.get(id=server_id)
        import requests
        query = {'id': plotter.server_number,'type': 'plotter'}
        response = requests.get('http://127.0.0.1:8080/icinga2/pki/ticket', params=query)
        messages.info(request,  '%s %s' % (plotter.server_name(),response.content))
        return HttpResponseRedirect(previous_url)

    def apply_plot_config(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        api = PlotterAPI(plotter)
        result = api.apply_plot_config()
        messages.info(request,  '%s %s' % (plotter.server_name(),result['msg']))
        return HttpResponseRedirect(previous_url)

    def start_sending(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        if plotter.harvester is None:
            messages.info(request, '%s has not bind with harvester' % plotter.server_name())
            return HttpResponseRedirect(previous_url)

        if plotter.harvester.internal_ip is None or plotter.harvester.internal_ip == '':
            messages.info(request, '%s internal_ip is not avabile' % plotter.harvester.server_name())
            return HttpResponseRedirect(previous_url)

        api = PlotterAPI(plotter)
        result = api.start_sending_process(plotter.harvester)

        messages.info(request, '%s %s' % (plotter.server_name(), result['msg']))
        return HttpResponseRedirect(previous_url)

    def stop_sending(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        api = PlotterAPI(plotter)
        result = api.stop_sending_process()
        messages.info(request, '%s %s' % (plotter.server_name(), result['msg']))
        return HttpResponseRedirect(previous_url)


class PlotConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'k', 'e', 'n_threads', 'n_buckets', 'job_buffer', 'global_max_jobs', 'global_stagger_m',
                    'tmpdir_max_jobs', 'tmpdir_stagger_phase_major', 'tmpdir_stagger_phase_minor', 'tmpdir_stagger_phase_limit', 'jobs_per_day','max_threads')
    list_filter = ('cache_type',)
    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                "fields": [
                    'name', 'cache_type', 'description'
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

class HarvesterAdmin(admin.ModelAdmin):
    list_display = ('server_number', 'internal_ip', 'plot_cnt', 'driver_cnt', 'harvester_action')

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                "fields": [
                    'server_number', 'description'
                ]
            }),
        )

    def harvester_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">U</a>&nbsp;'
            '<a class="button" href="{}">T</a>&nbsp;'
            '<a class="button" href="{}">N</a>&nbsp;'
            '<a class="button" href="{}">Hpool(R)</a>&nbsp;'
            '<a class="button" href="{}">StopNC</a>&nbsp;',
            reverse('admin:harvester-update-system', args=[obj.pk]),
            reverse('admin:harvester-pki-ticket', args=[obj.pk]),
            reverse('admin:harvester-update-nagios', args=[obj.pk]),
            reverse('admin:harvester-restart-hpool', args=[obj.pk]),
            reverse('admin:harvester-stop-nc', args=[obj.pk]),
        )

    harvester_action.allow_tags = True
    harvester_action.short_description = "Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(HarvesterAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<server_id>.+)/update-system/$',
                self.admin_site.admin_view(self.update_system),
                name='harvester-update-system',
            ),
            url(
                r'^(?P<server_id>.+)/restart-hpool/$',
                self.admin_site.admin_view(self.restart_hpool),
                name='harvester-restart-hpool',
            ),
            url(
                r'^(?P<server_id>.+)/stop-nc/$',
                self.admin_site.admin_view(self.stop_nc),
                name='harvester-stop-nc',
            ),

            url(
                r'^(?P<server_id>.+)/update-nagios/$',
                self.admin_site.admin_view(self.update_nagios_config),
                name='harvester-update-nagios',
            ),
            url(
                r'^(?P<server_id>.+)/pki-ticket/$',
                self.admin_site.admin_view(self.pki_ticket),
                name='harvester-pki-ticket',
            ),
        ]

        return my_urls + urls

    def update_system(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .harvester_api import HarvesterAPI
        harvester = Harvester.objects.get(id=server_id)
        api = HarvesterAPI(harvester)
        result = api.update_system()
        messages.info(request, '%s %s' % (harvester.server_name(), result['msg']))
        return HttpResponseRedirect(previous_url)

    def update_nagios_config(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        harvester = Harvester.objects.get(id=server_id)
        subprocess.check_output(["/etc/icinga2/zones.d/master/config_plotter.sh", "%s" % harvester.server_number])
        msg = "update config for plotter-%s success" % server_id
        messages.info(request, '%s %s' % (harvester.server_name(), msg))
        return HttpResponseRedirect(previous_url)

    def pki_ticket(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        harvester = Harvester.objects.get(id=server_id)
        logger.info("generate ticket for %s" % harvester.server_name())
        result = subprocess.check_output(["icinga2", "pki", "ticket", "--cn", harvester.server_name()])
        messages.info(request, '%s ticket: %s' % (harvester.server_name(), result))
        return HttpResponseRedirect(previous_url)

    def restart_hpool(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .harvester_api import HarvesterAPI
        harvester = Harvester.objects.get(id=server_id)
        api = HarvesterAPI(harvester)
        result = api.restart_service('srv.hpool')
        messages.info(request, '%s %s' % (harvester.server_name(), result['msg']))
        return HttpResponseRedirect(previous_url)

    def stop_nc(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .harvester_api import HarvesterAPI
        harvester = Harvester.objects.get(id=server_id)
        api = HarvesterAPI(harvester)
        result = api.stop_nc()
        messages.info(request, '%s %s' % (harvester.server_name(), result['msg']))
        return HttpResponseRedirect(previous_url)


class PlotTransferAdmin(admin.ModelAdmin):
    list_display = ('get_file_title', 'plotter_server', 'plotter_ip', 'harvester_server', 'harvester_ip', 'txn_start_time', 'txn_stop_time', 'plot_check', 'plot_check_fail_reason')


admin.site.register(Plotter, PlotterAdmin)
admin.site.register(PlotConfig, PlotConfigAdmin)
admin.site.register(Harvester, HarvesterAdmin)
admin.site.register(PlotTransfer, PlotTransferAdmin)