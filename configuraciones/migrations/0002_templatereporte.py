# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateReporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reporte_url', models.URLField(db_index=True)),
                ('asunto_reporte', models.CharField(max_length=240, db_index=True)),
                ('template_html', models.TextField()),
            ],
        ),
    ]
