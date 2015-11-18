# -*- coding: utf-8 -*-


from django.db import models


from empresas.models import Empresa


TIPOS_RECEPTORES = (
    ('dte', 'dte'), 
    ('cliente', 'cliente'),
)
TIPOS_ENVIOS = (
    ('notificacion', 'notificacion'),
    ('aceptacion', 'aceptacion'),
    ('rechazo', 'rechazo'),
    ('rems', 'rems'),
)
TIPOS_ESTADOS_DOCUMENTOS = (
    ('recepcionado', 'recepcionado'),
    ('no recepcionado', 'no recepcionado'),
    ('aceptado', 'aceptado'),
    ('rechazado', 'rechazado'),
)
TIPOS_OPERACIONES = (
    ('compra', 'compra'),
    ('venta', 'venta'),
)


class Email(models.Model):
	# campos basicos
    input_datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    input_date = models.DateField(auto_now_add=True, auto_now=False)
    # campos dte
    empresa = models.ForeignKey(Empresa)
    rut_receptor = models.CharField(max_length=20)
    rut_emisor = models.CharField(max_length=20)
    tipo_envio = models.CharField(max_length=20, choices=TIPOS_ENVIOS)
    tipo_dte = models.CharField(max_length=20)
    numero_folio = models.IntegerField()
    resolucion_receptor = models.CharField(max_length=20)
    resolucion_emisor = models.CharField(max_length=20)
    monto = models.IntegerField(default=0)
    fecha_emision = models.DateTimeField(null=True)
    fecha_recepcion = models.DateTimeField(null=True)
    estado_documento = models.CharField(max_length=100, choices=TIPOS_ESTADOS_DOCUMENTOS)
    tipo_operacion = models.CharField(max_length=100, choices=TIPOS_OPERACIONES)
    tipo_receptor = models.CharField(max_length=100, choices=TIPOS_RECEPTORES)
    # campos correo
    nombre_cliente = models.CharField(max_length=200)
    correo = models.EmailField(max_length=100)
    asunto = models.CharField(max_length=200)
    html = models.TextField()
    # adjuntos
    # attachs = models.KeyProperty(kind='AttachModel', repeated=True)
    # campos de processed
    smtp_id = models.CharField(max_length=200)
    processed_date = models.DateTimeField(null=True)
    processed_event = models.CharField(max_length=240)
    processed_sg_event_id = models.CharField(max_length=240)
    processed_sg_message_id = models.CharField(max_length=240)
    # campos delivered
    delivered_date = models.DateTimeField(null=True)
    delivered_event = models.CharField(max_length=240)
    delivered_sg_event_id = models.CharField(max_length=240)
    delivered_sg_message_id = models.CharField(max_length=240)
    delivered_response = models.TextField()
    # campos open
    opened_first_date = models.DateTimeField(null=True)
    opened_last_date = models.DateTimeField(null=True)
    opened_event = models.CharField(max_length=240)
    opened_ip = models.CharField(max_length=100)
    opened_user_agent = models.CharField(max_length=240)
    opened_sg_event_id = models.CharField(max_length=240)
    opened_sg_message_id = models.CharField(max_length=240)
    opened_count = models.IntegerField()
    # campos dropped
    dropped_date = models.DateTimeField(null=True)
    dropped_sg_event_id = models.CharField(max_length=240)
    dropped_sg_message_id = models.CharField(max_length=240)
    dropped_reason = models.CharField(max_length=240)
    dropped_event = models.CharField(max_length=240)
    # campos bounce
    bounce_date = models.DateTimeField(null=True)
    bounce_event = models.CharField(max_length=240)
    bounce_sg_event_id = models.CharField(max_length=240)
    bounce_sg_message_id = models.CharField(max_length=240)
    bounce_reason = models.TextField()
    bounce_status = models.CharField(max_length=240)
    bounce_type = models.CharField(max_length=240)
    # campos unscribes
    unsubscribe_date = models.DateTimeField(null=True)
    unsubscribe_uid = models.CharField(max_length=240)
    unsubscribe_purchase = models.CharField(max_length=240)
    unsubscribe_id = models.CharField(max_length=240)
    unsubscribe_event = models.CharField(max_length=240)
    # campos click
    click_ip = models.CharField(max_length=100)
    click_purchase = models.CharField(max_length=240)
    click_useragent = models.CharField(max_length=240)
    click_event = models.CharField(max_length=240)
    click_email = models.CharField(max_length=240)
    click_date = models.DateTimeField(null=True)
    click_url = models.CharField(max_length=240)

    def __unicode__(self):
    	return self.input_date + " " + self.correo + " " + self.numero_folio