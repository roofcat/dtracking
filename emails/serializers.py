# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer


from .models import Email


class EmailSerializer(ModelSerializer):

	class Meta:
		model = Email
		fields = ('id', 'input_date', 'input_datetime',
		    'empresa', 'rut_receptor', 'rut_emisor', 'tipo_envio', 'tipo_dte',
		    'numero_folio', 'resolucion_receptor', 'resolucion_emisor',
		    'monto', 'fecha_emision', 'fecha_recepcion', 'estado_documento',
		    'tipo_operacion', 'tipo_receptor', 'nombre_cliente',
		    'correo', 'asunto', 'html',
		)
