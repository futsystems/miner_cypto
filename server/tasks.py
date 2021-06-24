#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver
from common.mail import send_email, get_stuff_emails

import logging

logger = logging.getLogger(__name__)


def send_report():
    emails = get_stuff_emails()
    logger.info('emails:%s' % emails)

    import datetime
    from django.utils import timezone
    from models import HarvesterService, Harvester, PlotTransfer
    services = HarvesterService.objects.all()
    harvesters = Harvester.objects.all()
    local_power = sum([s.local_power for s in services])
    remote_power = sum([s.remote_power for s in services])

    driver_cnt = sum(([h.driver_cnt for h in harvesters]))
    total_current_plots = sum(([h.total_current_plots for h in harvesters]))
    space_free_plots = sum(([h.space_free_plots for h in harvesters]))

    last_day = timezone.now() - datetime.timedelta(days=1)
    logger.info('last day:%s' % last_day)

    txns = PlotTransfer.objects.filter(txn_stop_time__gte=last_day).all()
    plots_transfered = len(txns)

    subject = 'chia report daily'
    body = 'local power:%s\nremote power:%s\nratio:%s\n-------------------\ndriver_cnt:%s\nplots:%s\nplots_free:%s\n-------------------\nplots transfered:%s\n' % (local_power,
                                                                                                    remote_power,
                                                                                                    round(remote_power/local_power,2),
                                                                                                    driver_cnt,
                                                                                                    total_current_plots,
                                                                                                    space_free_plots,
                                                                                                    plots_transfered)

    for email in emails:
        send_email(subject, body, email)