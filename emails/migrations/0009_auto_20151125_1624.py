# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0008_auto_20151125_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(default=b'', null=True, upload_to=b'adjuntos/%Y/%m/%d/1448479481', blank=True),
        ),
    ]
