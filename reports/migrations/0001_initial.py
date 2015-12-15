# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_date', models.DateField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(max_length=120)),
                ('report', models.FileField(upload_to=b'reportes/%Y/%m/%d/1450191399')),
            ],
        ),
    ]
