# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0002_templatereporte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatereporte',
            name='reporte_url',
            field=models.URLField(null=True, db_index=True),
        ),
    ]
