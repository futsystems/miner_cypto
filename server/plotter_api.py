#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from server.models import Plotter

class PlotterAPI(object):
    def __init__(self, plotter):
        self._plotter = plotter
        self._host = plotter.api_host
        self._port = plotter.api_port

    def restart_service(self, service_name):
        query = {'service_name': service_name}
        response = requests.get('http://%s:%s/service/restart' % (self._host, self._port), params=query)

        return response.json()

    def apply_plot_config(self):
        response = requests.get('http://%s:%s/config/plotman/apply' % (self._host, self._port))
        return response.json()