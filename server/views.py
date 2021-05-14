#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from common import json_response
from server.models import Plotter
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