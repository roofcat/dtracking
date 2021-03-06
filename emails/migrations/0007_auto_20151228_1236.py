# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0006_auto_20151228_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(blank=True, default=b'', null=True, upload_to=b'adjuntos/%Y/%m/%d/1451317009'),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_receptor',
            field=models.CharField(blank=True, choices=[(b'electr\xc3\xb3nico', b'electr\xc3\xb3nico'), (b'manual', b'manual'), (b'ambos', b'ambos')], max_length=100, null=True),
        ),
    ]
