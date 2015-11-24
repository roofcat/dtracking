# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_auto_20151124_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='input_date',
            field=models.DateField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='input_datetime',
            field=models.DateTimeField(editable=False, db_index=True),
        ),
    ]
