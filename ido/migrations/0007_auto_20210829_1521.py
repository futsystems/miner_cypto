# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-29 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ido', '0006_token_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='platform',
            field=models.CharField(choices=[(b'CoinList', b'CoinList'), (b'Miso', b'Miso'), (b'DaoMaker', b'DaoMaker'), (b'LaunchZone', b'LaunchZone'), (b'FTX', b'FTX')], default=b'CoinList', max_length=10),
        ),
    ]
