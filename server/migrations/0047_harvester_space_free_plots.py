# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-18 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0046_auto_20210618_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='harvester',
            name='space_free_plots',
            field=models.IntegerField(default=0, verbose_name=b'Free Plots'),
        ),
    ]