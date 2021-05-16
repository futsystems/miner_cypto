# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-16 01:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20210516_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotter',
            name='st_avg_copy_time',
            field=models.FloatField(default=0, verbose_name=b'Copy Time'),
        ),
        migrations.AlterField(
            model_name='plotter',
            name='st_avg_plot_time',
            field=models.FloatField(default=0, verbose_name=b'Plot Time'),
        ),
        migrations.AlterField(
            model_name='plotter',
            name='st_plot_output',
            field=models.IntegerField(default=0, verbose_name=b'Output)'),
        ),
        migrations.AlterField(
            model_name='plotter',
            name='st_plot_process_cnt',
            field=models.IntegerField(default=0, verbose_name=b'Process'),
        ),
        migrations.AlterField(
            model_name='plotter',
            name='st_update_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name=b'UpdateTime'),
        ),
    ]
