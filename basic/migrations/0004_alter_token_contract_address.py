# Generated by Django 3.2.7 on 2021-09-02 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_auto_20210902_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='contract_address',
            field=models.CharField(default='--', max_length=50, verbose_name='Contract Address'),
        ),
    ]