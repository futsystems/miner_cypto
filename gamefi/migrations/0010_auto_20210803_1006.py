# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-03 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefi', '0009_auto_20210803_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='last_game_token_balance',
            field=models.FloatField(default=0, verbose_name=b'Game Token Balance(Last)'),
        ),
    ]
