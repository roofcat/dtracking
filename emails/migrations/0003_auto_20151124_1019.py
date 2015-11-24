# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_auto_20151119_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='bounce_event',
            field=models.CharField(db_index=True, max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_event',
            field=models.CharField(db_index=True, max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='correo',
            field=models.EmailField(max_length=100, db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='delivered_event',
            field=models.CharField(db_index=True, max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='dropped_event',
            field=models.CharField(db_index=True, max_length=240, null=True, blank=True),
        ),
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
        migrations.AlterField(
            model_name='email',
            name='monto',
            field=models.IntegerField(default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='numero_folio',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_event',
            field=models.CharField(db_index=True, max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='processed_event',
            field=models.CharField(db_index=True, max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='rut_emisor',
            field=models.CharField(max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='rut_receptor',
            field=models.CharField(max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_dte',
            field=models.CharField(max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_envio',
            field=models.CharField(db_index=True, max_length=20, choices=[(b'notificacion', b'notificacion'), (b'aceptacion', b'aceptacion'), (b'rechazo', b'rechazo'), (b'rems', b'rems')]),
        ),
        migrations.AlterField(
            model_name='email',
            name='unsubscribe_event',
            field=models.CharField(db_index=True, max_length=240, null=True, blank=True),
        ),
    ]
