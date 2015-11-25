# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0006_remove_email_input_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(default=datetime.datetime(2015, 11, 25, 14, 36, 32, 154000, tzinfo=utc), upload_to=b'adjuntos'),
            preserve_default=False,
        ),
    ]
