# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-04 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefi', '0013_game_token_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='chain_price',
            field=models.FloatField(default=0, verbose_name=b'Chain Price'),
        ),
    ]
