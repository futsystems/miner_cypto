# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-22 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0021_auto_20210522_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotter',
            name='memory_total',
            field=models.BigIntegerField(default=0, verbose_name=b'Memory Total'),
        ),
        migrations.AlterField(
            model_name='plotter',
            name='memory_used',
            field=models.BigIntegerField(default=0, verbose_name=b'Memory Used'),
        ),
    ]