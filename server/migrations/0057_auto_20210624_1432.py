# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-24 06:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0056_auto_20210624_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='HarvesterServiceRestart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(default=b'001', max_length=50, verbose_name=b'Service Name')),
                ('reason', models.CharField(default=b'001', max_length=50, verbose_name=b'Reason')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name=b'Restart Time')),
                ('harvester', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.Harvester', verbose_name=b'Harvester')),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.AlterModelOptions(
            name='harvesterservice',
            options={'ordering': ['index']},
        ),
        migrations.AlterField(
            model_name='harvesterservice',
            name='harvester',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='server.Harvester', verbose_name=b'Harvester'),
        ),
    ]
