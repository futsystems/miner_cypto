# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-16 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_auto_20210516_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotter',
            name='harvester',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.Harvester', verbose_name=b'Harvester'),
        ),
    ]
