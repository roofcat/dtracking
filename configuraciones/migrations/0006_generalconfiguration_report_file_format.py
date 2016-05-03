# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-03 17:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0005_auto_20160502_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalconfiguration',
            name='report_file_format',
            field=models.CharField(choices=[(b'xlsx', b'xlsx'), (b'csv', b'csv')], default=datetime.datetime(2016, 5, 3, 17, 25, 55, 392891, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]