# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0005_auto_20151221_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/%Y/%m/%d/1451300249'),
        ),
        migrations.AlterField(
            model_name='email',
            name='resolucion_emisor',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='resolucion_receptor',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]