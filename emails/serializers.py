# -*- coding: utf-8 -*-


from rest_framework import serializers


from .models import Email


class EmailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Email
		fields = ('input_date', 'input_datetime',
		    'empresa', 'rut_receptor', 'rut_emisor', 'tipo_envio', 'tipo_dte',
		    'numero_folio', 'resolucion_receptor', 'resolucion_emisor',
		    'monto', 'fecha_emision', 'fecha_recepcion', 'estado_documento',
		    'tipo_operacion', 'tipo_receptor', 'nombre_cliente',
		    'correo', 'asunto', 'html',
		)
