# -*- coding: utf-8 -*-


from django.contrib import admin

# Register your models here.

from django.conf.urls import url
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404 ,HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.admin.helpers import ActionForm
from django.contrib import admin,messages
from django.db import connection
from django.utils.html import format_html
from django import forms
from django.db.models import Max
from collections import OrderedDict
import subprocess
import logging,traceback,json
logger = logging.getLogger(__name__)

from server.models import Plotter, PlotConfig, Harvester, PlotTransfer, PlotKey, HarvesterService, HarvesterServiceRestart



def update_plotter(modeladmin, request, queryset):
    for plotter in queryset.all():
        if plotter.is_online:
            plotter.update_system()
update_plotter.short_description = "Update Plotter"

class PlotterAdmin(admin.ModelAdmin):
    list_display = ('server_number', 'cache', 'plot_config_content', 'job_plot',
                    'time_round', 'output', 'cpu', 'mem', 'thread', '_is_online', 'up_time', 'is_plotting_run', 'is_monero_run', 'plot_cnt', 'is_sending_run', 'dest_nas', 'plotter_action')
    ordering = ('server_number',)
    list_filter = ('harvester',)
    search_fields = ('server_number', 'description')
    actions = [update_plotter]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['server_number', 'plot_config_applied', 'internal_ip', 'boot_time', 'last_heartbeat', 'cpu_model', 'cpu_cnt', 'cpu_used_percent', 'memory_total', 'memory_used', 'nvme_cnt', 'nvme_size', 'is_cache_raid']

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                "fields": [
                    'server_number', 'plot_config', 'exclude_plot_dst_path', 'plot_file_path', 'plot_file_path_expand', 'data_interface', 'description'
                ]
            }),

            ("Harvester", {
                'fields': [
                    'harvester'
                ]
            }),

            ("Others", {
                'fields': [
                    'is_plotting_run', 'is_sending_run', 'is_monero_run'
                ]
            }),

            ("Info", {
                'fields': [
                    'internal_ip', 'boot_time', 'last_heartbeat',
                ]
            }),

            ("Hardware", {
                'fields': [
                    'cpu_model', 'cpu_cnt', 'cpu_used_percent', 'memory_total', 'memory_used', 'nvme_cnt', 'nvme_size', 'is_cache_raid'
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
            '<a class="button" href="{}">Shutdown</a>&nbsp;',
            reverse('admin:update-system', args=[obj.pk]),
            reverse('admin:pki-ticket', args=[obj.pk]),
            reverse('admin:update-nagios', args=[obj.pk]),
            reverse('admin:restart-hpool', args=[obj.pk]),
            reverse('admin:apply-plot-config', args=[obj.pk]),
            reverse('admin:plotter-shutdown', args=[obj.pk]),
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
            url(
                r'^(?P<server_id>.+)/plotter-shutdown/$',
                self.admin_site.admin_view(self.shutdown),
                name='plotter-shutdown',
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

        messages.info(request, '%s start sending plot' % (plotter.server_name()))
        return HttpResponseRedirect(previous_url)


    def stop_sending(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        api = PlotterAPI(plotter)
        result = api.stop_sending_process()
        messages.info(request, '%s stop sending plot' % (plotter.server_name()))
        return HttpResponseRedirect(previous_url)


    def shutdown(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        from .plotter_api import PlotterAPI
        plotter = Plotter.objects.get(id=server_id)
        api = PlotterAPI(plotter)
        result = api.shutdown()
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


class HarvesterServiceAdmin(admin.ModelAdmin):
    list_display = ('index', 'service', 'remote_power', 'remote_unit', 'local_power', 'ratio', 'status', 'harvester', 'harvester_service_action')
    list_filter = ('harvester',)
    def harvester_service_action(self, obj):
        """

        """
        return format_html(
            '<a class="button" href="{}">Restart</a>&nbsp;',
            reverse('admin:harvester-service-restart', args=[obj.pk]),
        )

    harvester_service_action.allow_tags = True
    harvester_service_action.short_description = "Action"

    def get_urls(self):
        # use get_urls for easy adding of views to the admin
        urls = super(HarvesterServiceAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<service_id>.+)/harvester-service-restart/$',
                self.admin_site.admin_view(self.restart_harvester_service),
                name='harvester-service-restart',
            ),
        ]

        return my_urls + urls

    def restart_harvester_service(self, request, service_id):
        previous_url = request.META.get('HTTP_REFERER')
        obj = HarvesterService.objects.get(id=service_id)
        from .harvester_api import HarvesterAPI
        api = HarvesterAPI(obj.harvester)
        result = api.restart_harvester(obj.service)
        messages.info(request, 'restart %s success' % obj.service)
        return HttpResponseRedirect(previous_url)


class HarvesterServiceRestartAdmin(admin.ModelAdmin):
    list_display = ('service', 'harvester', 'time', 'reason')



class HarvesterAdmin(admin.ModelAdmin):
    list_display = ('server_number', 'biz_ip', 'data_ip', 'driver_cnt', 'file_cnt', 'power', 'space_free_plots', 'plotter_cnt', 'nc_process_cnt',  '_is_online', 'up_time', 'harvester_action')
    ordering = ('server_number',)
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['server_number', 'biz_ip', 'biz_interface', 'data_ip', 'data_interface', 'boot_time', 'last_heartbeat', 'cpu_model', 'cpu_cnt', 'cpu_used_percent', 'memory_total', 'memory_used']


    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                "fields": [
                    'server_number', 'description'
                ]
            }),

            ("Others", {
                'fields': [
                    'auto_scan_plot'
                ]
            }),

            ("Info", {
                'fields': [
                    'biz_ip', 'biz_interface', 'data_ip', 'data_interface', 'boot_time', 'last_heartbeat',
                ]
            }),

            ("Hardware", {
                'fields': [
                    'cpu_model', 'cpu_cnt', 'cpu_used_percent', 'memory_total', 'memory_used'
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
        subprocess.check_output(["/etc/icinga2/zones.d/master/config_harvester.sh", "%s" % harvester.server_number])
        msg = "update config for harvester-%s success" % server_id
        messages.info(request, '%s %s' % (harvester.server_name(), msg))
        return HttpResponseRedirect(previous_url)

    def pki_ticket(self, request, server_id):
        previous_url = request.META.get('HTTP_REFERER')
        harvester = Harvester.objects.get(id=server_id)
        import requests
        query = {'id': harvester.server_number, 'type': 'harvester'}
        response = requests.get('http://127.0.0.1:8080/icinga2/pki/ticket', params=query)
        messages.info(request, '%s %s' % (harvester.server_name(), response.content))
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



class PlotKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer_pk', 'pool_key', 'description')


admin.site.register(Plotter, PlotterAdmin)
admin.site.register(PlotConfig, PlotConfigAdmin)
admin.site.register(Harvester, HarvesterAdmin)
admin.site.register(PlotTransfer, PlotTransferAdmin)
admin.site.register(PlotKey, PlotKeyAdmin)
admin.site.register(HarvesterService, HarvesterServiceAdmin)
admin.site.register(HarvesterServiceRestart, HarvesterServiceRestartAdmin)