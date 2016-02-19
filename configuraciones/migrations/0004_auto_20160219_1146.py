# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0003_soapwebservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='soapwebservice',
            name='campos_objeto_documento',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='soapwebservice',
            name='con_objeto_documento',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='soapwebservice',
            name='nombre_objeto_documento',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='soapwebservice',
            name='parametros_objeto_documento',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
