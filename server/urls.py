# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from server import views

urlpatterns = [
    url(r'^plotter/register$', views.register_plotter, name='plotter_register'),#注册P盘机
    url(r'^plotter/info$', views.get_plotter_info, name='plotter_info'),#查询P盘机信息
    url(r'^plotter/plot-config$', views.get_plot_config, name='plotter_plot_config'),#查询P盘参数
    url(r'^plotter/statistic/update$', views.update_plot_statistic, name='plotter_update_statistic'),#更新统计信息
    url(r'^plotter/local-info/update$', views.update_plot_info, name='plotter_update_info'),#更新本地状态信息
    url(r'^harvester/local-info/update$', views.update_harvester_info, name='harvester_update_info'),
    url(r'^transfer/start$', views.plot_transfer_start, name='plot_transfer_start'),
    url(r'^transfer/stop$', views.plot_transfer_stop, name='plot_transfer_stop'),
]