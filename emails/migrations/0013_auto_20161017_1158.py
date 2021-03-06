# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-17 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0012_auto_20160830_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='opcional1',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='opcional2',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='opcional3',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/ad1/%Y/%m/%d/1476716303'),
        ),
        migrations.AlterField(
            model_name='email',
            name='id_envio',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='pdf',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/pdf/%Y/%m/%d/1476716303'),
        ),
        migrations.AlterField(
            model_name='email',
            name='xml',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/xml/%Y/%m/%d/1476716303'),
        ),
    ]
