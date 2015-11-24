# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer


from .models import Email
from empresas.serializers import EmpresaSerializer


class EmailSerializer(ModelSerializer):
	# agregando el serializador de empresa
	# anida la relación en el json de listado
	# del modelo emails
	# empresa = EmpresaSerializer()

	class Meta:
		model = Email
		fields = ('id', 'input_date', 'empresa', 'rut_receptor', 
			'rut_emisor', 'tipo_envio', 'tipo_dte', 'numero_folio', 
			'resolucion_receptor', 'resolucion_emisor', 'monto', 'fecha_emision', 
			'fecha_recepcion', 'estado_documento', 'tipo_operacion', 'tipo_receptor', 
			'nombre_cliente', 'correo', 'asunto', 'html',
		)
