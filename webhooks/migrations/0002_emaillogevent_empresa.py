# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-09 14:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillogevent',
            name='empresa',
            field=models.CharField(default=datetime.datetime(2016, 5, 9, 14, 2, 54, 695962, tzinfo=utc), max_length=120),
            preserve_default=False,
        ),
    ]
