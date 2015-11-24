# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SendgridConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_key', models.CharField(max_length=200, db_index=True)),
                ('api_user', models.CharField(max_length=200, db_index=True)),
                ('api_pass', models.CharField(max_length=200, db_index=True)),
                ('asunto_email_dte', models.EmailField(max_length=240, db_index=True)),
                ('nombre_email_dte', models.CharField(max_length=200, db_index=True)),
                ('asunto_email_reporte', models.EmailField(max_length=240, db_index=True)),
                ('nombre_email_reporte', models.CharField(max_length=240, db_index=True)),
            ],
        ),
    ]
