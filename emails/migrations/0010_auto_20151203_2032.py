# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-03 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0009_auto_20151125_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/%Y/%m/%d/1449185563'),
        ),
    ]
