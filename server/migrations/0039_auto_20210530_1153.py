# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-30 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0038_auto_20210530_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='harvester',
            name='file_cnt',
            field=models.IntegerField(default=0, verbose_name=b'Files'),
        ),
        migrations.AlterField(
            model_name='harvester',
            name='driver_cnt',
            field=models.IntegerField(default=0, verbose_name=b'Drivers'),
        ),
        migrations.AlterField(
            model_name='harvester',
            name='plot_cnt',
            field=models.IntegerField(default=0, verbose_name=b'Plots'),
        ),
    ]
