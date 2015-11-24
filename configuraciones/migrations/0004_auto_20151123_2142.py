# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0003_auto_20151123_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatereporte',
            name='reporte_url',
            field=models.URLField(db_index=True, blank=True),
        ),
    ]
