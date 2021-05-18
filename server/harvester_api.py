#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from server.models import Plotter

class HarvesterAPI(object):
    def __init__(self, harvester):
        self._harvester = harvester
        self._host = harvester.api_host
        self._port = harvester.api_port

    def restart_service(self, service_name):
        """
        restart service srv.plotter srv.hpool etc
        :param service_name:
        :return:
        """
        query = {'service_name': service_name}
        response = requests.get('http://%s:%s/service/restart' % (self._host, self._port), params=query)

        return response.json()

    def update_system(self):
        """
        update plotter system
        :return:
        """
        response = requests.get('http://%s:%s/update' % (self._host, self._port))
        return response.json()


    def stop_nc(self):
        """
        stop nc process
        :return:
        """
        response = requests.get('http://%s:%s/nc/stop' % (self._host, self._port))
        return response.json()