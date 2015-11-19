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
    resolucion_receptor = models.CharField(
        max_length=20, null=True, blank=True)
    resolucion_emisor = models.CharField(max_length=20, null=True, blank=True)
    monto = models.IntegerField(default=0)
    fecha_emision = models.DateTimeField(null=True, blank=True)
    fecha_recepcion = models.DateTimeField(null=True, blank=True)
    estado_documento = models.CharField(
        max_length=100, choices=TIPOS_ESTADOS_DOCUMENTOS, null=True, blank=True)
    tipo_operacion = models.CharField(
        max_length=100, choices=TIPOS_OPERACIONES, null=True, blank=True)
    tipo_receptor = models.CharField(
        max_length=100, choices=TIPOS_RECEPTORES, null=True, blank=True)
    # campos correo
    nombre_cliente = models.CharField(max_length=200)
    correo = models.EmailField(max_length=100)
    asunto = models.CharField(max_length=200)
    html = models.TextField()
    # adjuntos
    # attachs = models.KeyProperty(kind='AttachModel', repeated=True)
    # campos de processed
    smtp_id = models.CharField(max_length=200, null=True, blank=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    processed_event = models.CharField(max_length=240, null=True, blank=True)
    processed_sg_event_id = models.CharField(max_length=240, null=True, blank=True)
    processed_sg_message_id = models.CharField(max_length=240, null=True, blank=True)
    # campos delivered
    delivered_date = models.DateTimeField(null=True, blank=True)
    delivered_event = models.CharField(max_length=240, null=True, blank=True)
    delivered_sg_event_id = models.CharField(max_length=240, null=True, blank=True)
    delivered_sg_message_id = models.CharField(max_length=240, null=True, blank=True)
    delivered_response = models.TextField(null=True, blank=True)
    # campos open
    opened_first_date = models.DateTimeField(null=True, blank=True)
    opened_last_date = models.DateTimeField(null=True, blank=True)
    opened_event = models.CharField(max_length=240, null=True, blank=True)
    opened_ip = models.CharField(max_length=100, null=True, blank=True)
    opened_user_agent = models.CharField(max_length=240, null=True, blank=True)
    opened_sg_event_id = models.CharField(max_length=240, null=True, blank=True)
    opened_sg_message_id = models.CharField(max_length=240, null=True, blank=True)
    opened_count = models.IntegerField(null=True, blank=True)
    # campos dropped
    dropped_date = models.DateTimeField(null=True, blank=True)
    dropped_sg_event_id = models.CharField(max_length=240, null=True, blank=True)
    dropped_sg_message_id = models.CharField(max_length=240, null=True, blank=True)
    dropped_reason = models.CharField(max_length=240, null=True, blank=True)
    dropped_event = models.CharField(max_length=240, null=True, blank=True)
    # campos bounce
    bounce_date = models.DateTimeField(null=True, blank=True)
    bounce_event = models.CharField(max_length=240, null=True, blank=True)
    bounce_sg_event_id = models.CharField(max_length=240, null=True, blank=True)
    bounce_sg_message_id = models.CharField(max_length=240, null=True, blank=True)
    bounce_reason = models.TextField(null=True, blank=True)
    bounce_status = models.CharField(max_length=240, null=True, blank=True)
    bounce_type = models.CharField(max_length=240, null=True, blank=True)
    # campos unscribes
    unsubscribe_date = models.DateTimeField(null=True, blank=True)
    unsubscribe_uid = models.CharField(max_length=240, null=True, blank=True)
    unsubscribe_purchase = models.CharField(max_length=240, null=True, blank=True)
    unsubscribe_id = models.CharField(max_length=240, null=True, blank=True)
    unsubscribe_event = models.CharField(max_length=240, null=True, blank=True)
    # campos click
    click_ip = models.CharField(max_length=100, null=True, blank=True)
    click_purchase = models.CharField(max_length=240, null=True, blank=True)
    click_useragent = models.CharField(max_length=240, null=True, blank=True)
    click_event = models.CharField(max_length=240, null=True, blank=True)
    click_email = models.CharField(max_length=240, null=True, blank=True)
    click_date = models.DateTimeField(null=True, blank=True)
    click_url = models.CharField(max_length=240, null=True, blank=True)

    def __unicode__(self):
        return u"{0} - {1}".format(self.correo, self.numero_folio)