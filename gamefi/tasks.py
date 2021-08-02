#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from common.mail import get_stuff_emails
from common.mail import send_email as _send_email


import logging
logger = logging.getLogger(__name__)



@shared_task
def sync_account_balance():
    logger.info('sync account balance')




