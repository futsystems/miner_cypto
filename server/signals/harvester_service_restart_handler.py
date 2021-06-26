#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from ..models import HarvesterServiceRestart
from django.dispatch import receiver
from common.mail import get_stuff_emails

import logging

logger = logging.getLogger(__name__)
from ..tasks import send_email

@receiver(post_save, sender=HarvesterServiceRestart)
def notify_harvester_service_restart(sender, instance, **kwargs):
    emails = get_stuff_emails()
    logger.info('emails:%s' % emails)
    for address in emails:
        send_email.delay('harvester service restart',  '%s / %s restart, reason:%s' % (instance.harvester, instance.service, instance.reason), address)
        #send_email('harvester service restart',
        #       '%s / %s restart, reason:%s' % (instance.harvester, instance.service, instance.reason),
        #        email)