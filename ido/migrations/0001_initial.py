# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-29 06:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'token', max_length=50, verbose_name=b'Name')),
                ('token', models.CharField(default=b'token', max_length=50, verbose_name=b'Token')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name=b'Date')),
                ('price', models.FloatField(default=0, verbose_name=b'Price')),
                ('quantity', models.FloatField(default=0, verbose_name=b'Quantity')),
                ('token_used', models.FloatField(default=0, verbose_name=b'Token Used')),
                ('token_type', models.CharField(choices=[(b'BTC', b'BTC'), (b'ETH', b'ETH'), (b'BNB', b'BNB')], default=b'ETH', max_length=10)),
                ('current_price', models.FloatField(default=0, verbose_name=b'Current Price')),
                ('description', models.CharField(blank=True, default=b'', max_length=1000, verbose_name=b'Description')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]