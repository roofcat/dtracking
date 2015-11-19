# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='bounce_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='bounce_event',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='bounce_reason',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='bounce_sg_event_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='bounce_sg_message_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='bounce_status',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='bounce_type',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_email',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_event',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_ip',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_purchase',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_url',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='click_useragent',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='delivered_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='delivered_event',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='delivered_response',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='delivered_sg_event_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='delivered_sg_message_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='dropped_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='dropped_event',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='dropped_reason',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='dropped_sg_event_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='dropped_sg_message_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='estado_documento',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'recepcionado', b'recepcionado'), (b'no recepcionado', b'no recepcionado'), (b'aceptado', b'aceptado'), (b'rechazado', b'rechazado')]),
        ),
        migrations.AlterField(
            model_name='email',
            name='fecha_emision',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='fecha_recepcion',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_event',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_first_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_ip',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_last_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_sg_event_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_sg_message_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='opened_user_agent',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='processed_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='processed_event',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='processed_sg_event_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='processed_sg_message_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='resolucion_emisor',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='resolucion_receptor',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='smtp_id',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_envio',
            field=models.CharField(max_length=20, choices=[(b'notificacion', b'notificacion'), (b'aceptacion', b'aceptacion'), (b'rechazo', b'rechazo'), (b'rems', b'rems')]),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_operacion',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'compra', b'compra'), (b'venta', b'venta')]),
        ),
        migrations.AlterField(
            model_name='email',
            name='tipo_receptor',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'dte', b'dte'), (b'cliente', b'cliente')]),
        ),
        migrations.AlterField(
            model_name='email',
            name='unsubscribe_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='unsubscribe_event',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='unsubscribe_id',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='unsubscribe_purchase',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='unsubscribe_uid',
            field=models.CharField(max_length=240, null=True, blank=True),
        ),
    ]
