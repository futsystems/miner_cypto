# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-29 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ido', '0005_auto_20210829_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='platform',
            field=models.CharField(choices=[(b'ETH', b'ETH'), (b'BNB', b'BNB'), (b'BNB', b'BNB')], default=b'ETH', max_length=10),
        ),
    ]
