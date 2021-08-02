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
from models.game import Game

def homepage(request):
    return 'gamefi'