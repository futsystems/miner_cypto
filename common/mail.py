#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import logging
import traceback

logger = logging.getLogger(__name__)

from django.contrib.auth import get_user_model
User = get_user_model()


def get_stuff_emails():
    users = User.objects.all()
    email_list = []
    for user in users:
        if user.is_staff:
            email_list.append(user.email)

    return email_list


def send_email(subject, body, receiver, receiver_name=''):
    if receiver_name is None or receiver_name == '':
        receiver_name = receiver.split('@')[0]

    try:
        requests.post(
            "https://api.mailgun.net/v3/notify.futsystems.com/messages",
            auth=("api", "784e1276bbaf231336571ac04c8c383e-8b7bf2f1-b6013475"),
            data={"from": "NOC <noc@notify.futsystems.com>",
                  "to": [receiver_name, receiver],
                  "subject": subject,
                  "text": body})
        return True
    except Exception as e:
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    send_email('subject', 'message body', '82431282@qq.com')

