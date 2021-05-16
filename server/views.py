#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from common import json_response, Success, Error
from server.models import Plotter, Harvester, PlotTransfer
import logging, traceback


import json
logger = logging.getLogger(__name__)


def get_plot_config(request):
    try:
        if request.method == "POST":
            raise Exception("POST not support")
        else:
            server_number = request.GET.get("id", None)
            plotter = Plotter.objects.get(server_number=server_number)
            plot_config_dict = plotter.get_plot_config_dict()
        return json_response(plot_config_dict)
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(e.message)

@csrf_exempt
def update_plot_statistic(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            logger.info(data)
            plotter_server_name = data['name']
            server_number = plotter_server_name.split('-')[1]

            try:
                plotter = Plotter.objects.get(server_number=server_number)
                plotter.update_statistic(data['statistic'])

            except Plotter.DoesNotExist as e:
                json_response(Error('Plotter do not exist'))
        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))

@csrf_exempt
def update_plot_info(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            logger.info(data)
            plotter_server_name = data['name']
            server_number = plotter_server_name.split('-')[1]

            try:
                plotter = Plotter.objects.get(server_number=server_number)
                plotter.update_local_info(data['info'])

            except Plotter.DoesNotExist as e:
                json_response(Error('Plotter do not exist'))
        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))


@csrf_exempt
def update_harvester_info(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            logger.info(data)
            harvester_server_name = data['name']
            server_number = harvester_server_name.split('-')[1]
            try:
                harvester = Harvester.objects.get(server_number=server_number)
                harvester.update_local_info(data['info'])

            except Harvester.DoesNotExist as e:
                json_response(Error('Harvester do not exist'))
        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))


@csrf_exempt
def plot_transfer_start(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            logger.info(data)

            plot_file_name = data['plot_file_name']
            plotter_server = data['plotter_server']
            plotter_ip = data['plotter_ip']
            harvester_server = data['harvester_server']
            harvester_ip = data['harvester_ip']
            txn_start_time = data['txn_start_time']

            PlotTransfer.objects.create(plot_file_name=plot_file_name,
                                       plotter_server=plotter_server,
                                       plotter_ip=plotter_ip,
                                       harvester_server=harvester_server,
                                       harvester_ip=harvester_ip,
                                       txn_start_time=txn_start_time)


        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))

@csrf_exempt
def plot_transfer_stop(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            logger.info(data)

            plot_file_name = data['plot_file_name']
            txn_stop_time = data['txn_stop_time']
            plot_check = data['plot_check']
            plot_check_fail_reason = data['plot_check_fail_reason']

            try:
                txn = PlotTransfer.objects.get(plot_file_name=plot_file_name)
                txn.txn_stop_time = txn_stop_time
                txn.plot_check = plot_check
                txn.plot_check_fail_reason = plot_check_fail_reason
            except PlotTransfer.DoesNotExist as e:
                json_response(Error('Plot Transfer do not exist'))

        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))

