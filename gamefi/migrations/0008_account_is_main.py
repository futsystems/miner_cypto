# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-02 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefi', '0007_auto_20210802_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name=b'Main Account'),
        ),
    ]