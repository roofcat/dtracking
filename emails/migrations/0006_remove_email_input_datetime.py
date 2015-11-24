# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0005_auto_20151124_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='input_datetime',
        ),
    ]
