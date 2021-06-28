#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from common import json_response, Success, Error
from server.models import Plotter, Harvester, PlotTransfer, HarvesterServiceRestart
import logging, traceback
import requests
from datetime import datetime

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


def get_plotter_config(request):
    try:
        if request.method == "POST":
            raise Exception("POST not support")
        else:
            server_number = request.GET.get("id", None)
            plotter = Plotter.objects.get(server_number=server_number)
            config = plotter.get_plotter_config_dict()
        return json_response(config)
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(e.message)


def get_harvester_config(request):
    try:
        if request.method == "POST":
            raise Exception("POST not support")
        else:
            server_number = request.GET.get("id", None)
            harvester = Harvester.objects.get(server_number=server_number)
            config = harvester.get_harvester_config_dict()
        return json_response(config)
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(e.message)


def get_plotter_info(request):
    try:
        if request.method == "POST":
            raise Exception("POST not support")
        else:
            server_number = request.GET.get("id", None)
            plotter = Plotter.objects.get(server_number=server_number)
        return json_response(Success(plotter.get_info()))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(e.message)


@csrf_exempt
def register_plotter(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)

            plotter_server_name = data['name']
            logger.info('%s register to manager node, data:%s' % (plotter_server_name, data))
            server_number = plotter_server_name.split('-')[1]
            try:
                plotter = Plotter.objects.get(server_number=server_number)
                #plotter 注册上线后 执行nagios配置更新
                query = {'id': plotter.server_number}
                response = requests.get('http://127.0.0.1:8080/icinga2/config/plotter', params=query)
                plotter.update_register(data)
                logger.info('%s is online' % plotter_server_name)
            except Plotter.DoesNotExist as e:
                json_response(Error('Plotter do not exist'))
        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))

@csrf_exempt
def register_harvester(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            harvester_server_name = data['name']
            logger.info('%s register to manager node, data:%s' % (harvester_server_name, data))
            server_number = harvester_server_name.split('-')[1]

            try:
                harvester = Harvester.objects.get(server_number=server_number)
                #plotter 注册上线后 执行nagios配置更新
                #query = {'id': harvester.server_number}
                #response = requests.get('http://127.0.0.1:8080/icinga2/config/plotter', params=query)
                harvester.update_register(data)
                logger.info('%s is online' % harvester_server_name)
            except Plotter.DoesNotExist as e:
                json_response(Error('Plotter do not exist'))
        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))

@csrf_exempt
def update_plot_statistic(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            #logger.info(data)
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
            #logger.info(data)
            plotter_server_name = data['name']
            server_number = plotter_server_name.split('-')[1]

            try:
                plotter = Plotter.objects.get(server_number=server_number)
                plotter.update_local_info(data)

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
                logging.info('harvester:%s report local info:%s' % (harvester_server_name, data))
                harvester = Harvester.objects.get(server_number=server_number)
                harvester.update_local_info(data)

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
            plotter_path = data['plotter_path']
            plotter_ip = data['plotter_ip']

            harvester_server = data['harvester_server']
            harvester_ip = data['harvester_ip']
            harvester_path = data['harvester_path']

            nc_pid = data['nc_pid']
            nc_port = data['nc_port']

            PlotTransfer.objects.create(plot_file_name=plot_file_name,
                                       plotter_server=plotter_server,
                                       plotter_ip=plotter_ip,
                                        plotter_path=plotter_path,
                                       harvester_server=harvester_server,
                                       harvester_ip=harvester_ip,
                                        harvester_path=harvester_path,
                                        nc_pid=nc_pid,
                                        nc_port=nc_port,
                                       txn_start_time= datetime.now())
        return json_response(Success(''))

    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error('plot transfer start server side error'))

@csrf_exempt
def plot_transfer_stop(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            logger.info(data)

            plot_file_name = data['plot_file_name']
            plot_check = data['plot_check']
            plot_check_fail_reason = data['plot_check_fail_reason']

            try:
                txn = PlotTransfer.objects.get(plot_file_name=plot_file_name)
                txn.txn_stop_time = datetime.now()
                txn.plot_check = plot_check
                txn.plot_check_fail_reason = plot_check_fail_reason
            except PlotTransfer.DoesNotExist as e:
                json_response(Error('Plot Transfer do not exist'))
        return json_response(Success(''))
    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error(e.message))


@csrf_exempt
def harvester_service_restart(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            logger.info(data)

            harvester = data['harvester']
            service = data['service']
            reason = data['reason']

            harvester = Harvester.objects.get(server_number=harvester.split('-')[1])
            obj = HarvesterServiceRestart.objects.create(reason=reason, service=service, harvester=harvester, time=timezone.now())
            #harvester_service_restart.send(obj)
        return json_response(Success(''))

    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error('plot transfer start server side error'))


@csrf_exempt
def demo_report(request):
    try:
        from tasks import send_reportget_plotter_config
        send_report()
        return json_response(Success(''))

    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error('demo report server side error'))

@csrf_exempt
def demo_task(request):
    try:
        from server import tasks
        logger.info('submit task')
        res = tasks.send_email.delay('subject', 'body', '82431282@qq.com')
        return json_response(Success(''))

    except Exception as e:
        logger.error(traceback.format_exc())
        return json_response(Error('demo report server side error'))
