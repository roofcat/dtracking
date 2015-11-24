# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0004_auto_20151124_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='input_date',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='input_datetime',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
