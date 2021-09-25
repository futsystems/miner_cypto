# Generated by Django 3.2.7 on 2021-09-02 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_token_chain_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='contract_address',
            field=models.CharField(default='Contract', max_length=50, verbose_name='Contract Address'),
        ),
        migrations.AlterField(
            model_name='token',
            name='chain_type',
            field=models.CharField(choices=[('MAIN', 'MAIN'), ('ETH', 'ETH'), ('BSC', 'BSC')], default='MAIN', max_length=10),
        ),
    ]