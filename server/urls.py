# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from server import views

urlpatterns = [
    url(r'^plotter/plot-config$', views.get_plot_config, name='plotter_plot_config'),
    url(r'^plotter/statistic/update$', views.update_plot_statistic, name='plotter_update_statistic'),
    url(r'^plotter/local-info/update$', views.update_plot_info, name='plotter_update_info'),
    url(r'^harvester/local-info/update$', views.update_harvester_info, name='harvester_update_info'),
    url(r'^transfer/start$', views.plot_transfer_start, name='plot_transfer_start'),
    url(r'^transfer/stop$', views.plot_transfer_stop, name='plot_transfer_stop'),
]