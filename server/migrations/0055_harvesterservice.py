# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-24 01:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0054_auto_20210621_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='HarvesterService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0, verbose_name=b'Index')),
                ('name', models.CharField(default=b'001', max_length=50, verbose_name=b'Service Name')),
                ('local_power', models.FloatField(default=0, verbose_name=b'Local Power')),
                ('remote_power', models.FloatField(default=0, verbose_name=b'Remote Power')),
                ('remote_unit', models.CharField(blank=True, default=b'TB', max_length=20, verbose_name=b'Remote Unit')),
                ('status', models.CharField(blank=True, default=b'', max_length=100, verbose_name=b'Status')),
                ('harvester', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='server.Harvester', verbose_name=b'PlotConfig')),
            ],
        ),
    ]
