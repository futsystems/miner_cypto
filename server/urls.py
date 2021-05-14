# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from server import views

urlpatterns = [
    url(r'^plotter/plot-config$', views.get_plot_config, name='plotter_plot_config'),
]