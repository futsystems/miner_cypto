#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from ..models import HarvesterServiceRestart
from django.dispatch import receiver
from common.mail import send_email, get_stuff_emails

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=HarvesterServiceRestart)
def notify_harvester_service_restart(sender, instance, **kwargs):
    emails = get_stuff_emails()
    logger.info('emails:%s' % emails)
    for email in emails:
        send_email('harvester service restart',
               '%s / %s restart, reason:%s' % (instance.harvester, instance.service, instance.reason),
                email)