# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-02 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefi', '0004_account_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='chain',
            field=models.CharField(choices=[(b'BSC', b'BSC'), (b'ETH', b'ETH')], default=b'BSC', max_length=10),
        ),
    ]