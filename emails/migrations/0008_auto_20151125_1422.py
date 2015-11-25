# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0007_email_adjunto1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='adjunto1',
            field=models.FileField(default=b'', null=True, upload_to=b'adjuntos/1448472168/', blank=True),
        ),
    ]
