# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-08 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EliminacionHistorico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=False)),
                ('dias_a_eliminar', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
