# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-30 01:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0037_auto_20210530_0933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='harvester',
            old_name='last_heartbeat_time',
            new_name='last_heartbeat',
        ),
    ]