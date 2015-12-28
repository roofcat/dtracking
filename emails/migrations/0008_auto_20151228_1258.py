# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0007_auto_20151228_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/%Y/%m/%d/1451318317'),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_envio',
            field=models.CharField(choices=[(b'aceptacion', b'aceptacion'), (b'envio dte', b'envio dte'), (b'notificacion', b'notificacion'), (b'rechazo', b'rechazo'), (b'rems', b'rems')], db_index=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_receptor',
            field=models.CharField(blank=True, choices=[(b'electronico', b'electronico'), (b'manual', b'manual'), (b'ambos', b'ambos')], max_length=100, null=True),
        ),
    ]
