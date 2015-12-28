# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer, FileField


from .models import Email


class EmailDteInputSerializer(ModelSerializer):
    # agregando el serializador de empresa
    # anida la relación en el json de listado
    # del modelo emails, pero en los parametros
    # rest hay que enviarlos
    # empresa = EmpresaSerializer()
    # tipo_dte = TipoDocumentoSerializer()
    adjunto1 = FileField(use_url=False, max_length=None,
                         allow_null=True, allow_empty_file=True)

    class Meta:
        model = Email
        fields = (
            'id', 'input_date', 'empresa', 'rut_receptor', 'rut_emisor', 
            'tipo_envio', 'tipo_dte', 'numero_folio', 'resolucion_receptor', 
            'resolucion_emisor', 'monto', 'fecha_emision', 'fecha_recepcion', 
            'estado_documento', 'id_envio', 'tipo_operacion', 'tipo_receptor',
            'nombre_cliente', 'correo', 'asunto', 'html', 'adjunto1'
        )
