# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-28 14:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0034_auto_20210528_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plotter',
            old_name='is_cache_raid0',
            new_name='is_cache_raid',
        ),
    ]
