# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('rut', models.CharField(max_length=20, unique=True, serialize=False, primary_key=True)),
                ('empresa', models.CharField(max_length=200)),
            ],
        ),
    ]
