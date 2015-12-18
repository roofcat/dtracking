# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_auto_20151217_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/%Y/%m/%d/1450463303'),
        ),
        migrations.AlterField(
            model_name='email',
            name='fecha_emision',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='fecha_recepcion',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='monto',
            field=models.BigIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='email',
            name='numero_folio',
            field=models.BigIntegerField(db_index=True),
        ),
    ]
