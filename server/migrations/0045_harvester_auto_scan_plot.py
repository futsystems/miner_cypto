# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-17 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0044_plotter_plot_file_path_expand'),
    ]

    operations = [
        migrations.AddField(
            model_name='harvester',
            name='auto_scan_plot',
            field=models.BooleanField(default=False, verbose_name=b'Auto Scan'),
        ),
    ]
