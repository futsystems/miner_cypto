# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-02 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefi', '0002_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_id',
            field=models.CharField(default=b'0', max_length=50, verbose_name=b'ID'),
        ),
    ]
