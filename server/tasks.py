#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver
from common.mail import send_email, get_stuff_emails

import logging

logger = logging.getLogger(__name__)
#!/usr/bin/python
# -*- coding: utf-8 -*-


def send_report():
    emails = get_stuff_emails()
    logger.info('emails:%s' % emails)

    import datetime
    from django.utils import timezone
    from .models import HarvesterService, Harvester, PlotTransfer
    services = HarvesterService.objects.all()
    harvesters = Harvester.objects.all()
    local_power = round(sum([s.local_power for s in services]), 2)
    remote_power = round(sum([s.remote_power for s in services]), 2)

    driver_cnt = sum(([h.driver_cnt for h in harvesters]))
    total_current_plots = sum(([h.total_current_plots for h in harvesters]))
    space_free_plots = sum(([h.space_free_plots for h in harvesters]))

    now = timezone.now()
    last_day = now - datetime.timedelta(days=1)
    #logger.info('last day:%s' % last_day)

    txns = PlotTransfer.objects.filter(txn_stop_time__gte=last_day).all()
    plots_transfered = len(txns)

    subject = 'chia daily report [%s]' % timezone.localtime(now).strftime('%Y-%m-%d %H:%M:%S')
    body = 'local power:%s\nremote power:%s\nratio:%s\n-------------------\ndriver_cnt:%s\nplots:%s\nplots_free:%s\n-------------------\nplots transfered:%s\n' % (local_power,
                                                                                                    remote_power,
                                                                                                    round(remote_power/local_power,2),
                                                                                                    driver_cnt,
                                                                                                    total_current_plots,
                                                                                                    space_free_plots,
                                                                                                    plots_transfered)

    for email in emails:
        send_email(subject, body, email)


def send_problem():
    emails = get_stuff_emails()
    logger.info('emails:%s' % emails)

    import datetime
    from django.utils import timezone
    from .models import Plotter, HarvesterService, Harvester, PlotTransfer

    subject = 'chia pending problems'
    body = ''


    # plotters缓存plots太多
    plotters = Plotter.objects.all()
    plotters_sending = [p for p in plotters if (p.harvester is not None and p.plot_cnt>=5)]
    if len(plotters_sending) > 0:
        body ='%s\nplotter overstock:' % body
        for plotter in plotters_sending:
            body = '%s%s ' % (body, plotter.server_number)

    # plotters开启时间超过4小时 但是CPU使用率一直偏低
    plotters_low_cpu = [p for p in plotters if (p.harvester is not None and (p.uptime/3600) > 4 and p.cpu_used_percent < 0.3 )]
    if len(plotters_low_cpu) > 0:
        body = '%s\nplotter low cpu:' % body
        for plotter in plotters_low_cpu:
            body = '%s%s ' % (body, plotter.server_number)


    if body != '':
        for email in emails:
            send_email(subject, body, email)



