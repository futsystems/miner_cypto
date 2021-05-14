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
            id = request.GET.get("id", None)
            ploter = Plotter.objects.get(id=id)
            plot_config = ploter.plot_config
        return json_response(plot_config.to_dict())
    except Exception, e:
        logger.error(traceback.format_exc())
        return json_response(e.message)