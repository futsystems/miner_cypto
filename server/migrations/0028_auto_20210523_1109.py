# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-23 03:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0027_plotter_exclude_dst_paths'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plotter',
            old_name='exclude_dst_paths',
            new_name='exclude_plot_dst_path',
        ),
    ]