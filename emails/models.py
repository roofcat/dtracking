# -*- coding: utf-8 -*-


from datetime import datetime
import calendar
import json
import logging


from django.db import models
from django.db.models import Count, Q
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict


from empresas.models import Empresa
from tipodocumentos.models import TipoDocumento


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
    # input_datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    input_date = models.DateField(auto_now_add=True, db_index=True)
    # campos dte
    empresa = models.ForeignKey(Empresa)
    rut_receptor = models.CharField(max_length=20, db_index=True)
    rut_emisor = models.CharField(max_length=20, db_index=True)
    tipo_envio = models.CharField(max_length=20,
                                  choices=TIPOS_ENVIOS,
                                  db_index=True)
    tipo_dte = models.ForeignKey(TipoDocumento)
    numero_folio = models.IntegerField(db_index=True)
    resolucion_receptor = models.CharField(max_length=20,
                                           null=True,
                                           blank=True)
    resolucion_emisor = models.CharField(max_length=20, null=True, blank=True)
    monto = models.IntegerField(default=0, db_index=True)
    fecha_emision = models.DateTimeField(null=True, blank=True)
    fecha_recepcion = models.DateTimeField(null=True, blank=True)
    estado_documento = models.CharField(max_length=100,
                                        choices=TIPOS_ESTADOS_DOCUMENTOS,
                                        null=True,
                                        blank=True)
    tipo_operacion = models.CharField(max_length=100,
                                      choices=TIPOS_OPERACIONES,
                                      null=True,
                                      blank=True)
    tipo_receptor = models.CharField(max_length=100,
                                     choices=TIPOS_RECEPTORES,
                                     null=True,
                                     blank=True)
    # campos correo
    nombre_cliente = models.CharField(max_length=200)
    correo = models.EmailField(max_length=100, db_index=True)
    asunto = models.CharField(max_length=200, blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    # adjuntos
    adjunto1 = models.FileField(
        upload_to='adjuntos/%Y/%m/%d/{0}'.format(
            calendar.timegm(datetime.utcnow().utctimetuple())),
        default='', null=True, blank=True)
    # campos de processed
    smtp_id = models.CharField(max_length=200, null=True, blank=True)
    processed_date = models.BigIntegerField(null=True, blank=True)
    processed_event = models.CharField(max_length=240,
                                       null=True,
                                       blank=True,
                                       db_index=True)
    processed_sg_event_id = models.CharField(max_length=240,
                                             null=True,
                                             blank=True)
    processed_sg_message_id = models.CharField(max_length=240,
                                               null=True,
                                               blank=True)
    # campos delivered
    delivered_date = models.BigIntegerField(null=True, blank=True)
    delivered_event = models.CharField(max_length=240,
                                       null=True,
                                       blank=True,
                                       db_index=True)
    delivered_sg_event_id = models.CharField(max_length=240,
                                             null=True,
                                             blank=True)
    delivered_sg_message_id = models.CharField(max_length=240,
                                               null=True,
                                               blank=True)
    delivered_response = models.TextField(null=True, blank=True)
    # campos open
    opened_first_date = models.BigIntegerField(null=True, blank=True)
    opened_last_date = models.BigIntegerField(null=True, blank=True)
    opened_event = models.CharField(max_length=240,
                                    null=True,
                                    blank=True,
                                    db_index=True)
    opened_ip = models.CharField(max_length=100, null=True, blank=True)
    opened_user_agent = models.CharField(max_length=240,
                                         null=True,
                                         blank=True)
    opened_sg_event_id = models.CharField(max_length=240,
                                          null=True,
                                          blank=True)
    opened_sg_message_id = models.CharField(max_length=240,
                                            null=True,
                                            blank=True)
    opened_count = models.IntegerField(null=True,
                                       blank=True,
                                       default=0)
    # campos dropped
    dropped_date = models.BigIntegerField(null=True, blank=True)
    dropped_sg_event_id = models.CharField(max_length=240,
                                           null=True,
                                           blank=True)
    dropped_sg_message_id = models.CharField(max_length=240,
                                             null=True,
                                             blank=True)
    dropped_reason = models.CharField(max_length=240, null=True, blank=True)
    dropped_event = models.CharField(max_length=240,
                                     null=True,
                                     blank=True,
                                     db_index=True)
    # campos bounce
    bounce_date = models.BigIntegerField(null=True, blank=True)
    bounce_event = models.CharField(max_length=240,
                                    null=True,
                                    blank=True,
                                    db_index=True)
    bounce_sg_event_id = models.CharField(max_length=240,
                                          null=True,
                                          blank=True)
    bounce_sg_message_id = models.CharField(max_length=240,
                                            null=True,
                                            blank=True)
    bounce_reason = models.TextField(null=True, blank=True)
    bounce_status = models.CharField(max_length=240, null=True, blank=True)
    bounce_type = models.CharField(max_length=240, null=True, blank=True)
    # campos unscribes
    unsubscribe_date = models.BigIntegerField(null=True, blank=True)
    unsubscribe_uid = models.CharField(max_length=240, null=True, blank=True)
    unsubscribe_purchase = models.CharField(max_length=240,
                                            null=True,
                                            blank=True)
    unsubscribe_id = models.CharField(max_length=240, null=True, blank=True)
    unsubscribe_event = models.CharField(max_length=240,
                                         null=True,
                                         blank=True,
                                         db_index=True)
    # campos click
    click_ip = models.CharField(max_length=100, null=True, blank=True)
    click_purchase = models.CharField(max_length=240, null=True, blank=True)
    click_useragent = models.CharField(max_length=240, null=True, blank=True)
    click_event = models.CharField(max_length=240,
                                   null=True,
                                   blank=True,
                                   db_index=True)
    click_email = models.CharField(max_length=240, null=True, blank=True)
    click_date = models.BigIntegerField(null=True, blank=True)
    click_url = models.CharField(max_length=240, null=True, blank=True)

    def __unicode__(self):
        return u"{0} - {1}".format(self.correo, self.numero_folio)

    # funcion utilizada desde el webhook rest
    @classmethod
    def get_email(self, email_id):
        try:
            email = Email.objects.get(pk=email_id)
            logging.info("Email Existe")
        except Email.DoesNotExist:
            logging.error("Email.DoesNotExist")
            email = None
        return email

    # funcion DRY para webhook api
    @classmethod
    def set_default_fields(body):
        email = Email.objects.create()
        email.empresa = str(body['empresa']).decode('utf-8')
        email.rut_receptor = str(body['rut_receptor']).decode('utf-8')
        email.rut_emisor = str(body['rut_emisor']).decode('utf-8')
        email.tipo_envio = str(body['tipo_envio']).decode('utf-8')
        email.tipo_dte = str(body['tipo_dte']).decode('utf-8')
        email.numero_folio = str(body['numero_folio']).decode('utf-8')
        email.resolucion_receptor = str(body['resolucion_receptor']).decode('utf-8')
        email.resolucion_emisor = str(body['resolucion_emisor']).decode('utf-8')
        email.monto = str(body['monto']).decode('utf-8')
        email.fecha_emision = str(body['fecha_emision']).decode('utf-8')
        email.fecha_recepcion = str(body['fecha_recepcion']).decode('utf-8')
        email.estado_documento = str(body['estado_documento']).decode('utf-8')
        email.tipo_operacion = str(body['tipo_operacion']).decode('utf-8')
        email.tipo_receptor = str(body['tipo_receptor']).decode('utf-8')
        email.nombre_cliente = str(body['nombre_cliente']).decode('utf-8')
        email.correo = str(body['correo']).decode('utf-8')
        return email

    # funcion utilizada desde el webhook api
    @classmethod
    def get_email(self, correo, numero_folio, tipo_dte):
        try:
            email = Email.objects.get(
                correo=correo, numero_folio=numero_folio, tipo_dte=tipo_dte)
            logging.info("Email Existe")
        except Email.DoesNotExist:
            logging.error("Email.DoesNotExist")
            email = None
        return email

    # MÉTODOS DE CONSULTAS (para no repetir código)
    @classmethod
    def get_statistics_count_by_dates(self, date_from, date_to):
        count_total = Email.objects.filter(
            input_date__range=(date_from, date_to)).count()
        count_processed = Email.objects.filter(
            input_date__range=(date_from, date_to),
            processed_event='processed').count()
        count_delivered = Email.objects.filter(
            input_date__range=(date_from, date_to),
            delivered_event='delivered').count()
        count_opened = Email.objects.filter(
            input_date__range=(date_from, date_to),
            opened_event='open').count()
        count_dropped = Email.objects.filter(
            input_date__range=(date_from, date_to),
            dropped_event='dropped').count()
        count_bounce = Email.objects.filter(
            input_date__range=(date_from, date_to),
            bounce_event='bounce').count()
        return {
            'total': count_total,
            'processed': count_processed,
            'delivered': count_delivered,
            'opened': count_opened,
            'dropped': count_dropped,
            'bounced': count_bounce,
        }

    @classmethod
    def get_statistics_range_by_dates(self, date_from, date_to):
        try:
            emails = Email.objects.filter(input_date__range=(
                date_from, date_to)).values('input_date').annotate(
                total=Count('input_date'), processed=Count('processed_event'),
                delivered=Count('delivered_event'), opened=Count('opened_event'),
                dropped=Count('dropped_event'), bounced=Count('bounce_event')
            ).order_by('input_date')
            data = []
            for email in emails:
                email = json.dumps(email, cls=DjangoJSONEncoder)
                data.append(json.loads(email))
            return data
        except Exception, e:
            print e

    @classmethod
    def get_delayed_emails(self):
        emails = Email.objects.filter(
            Q(processed_event__isnull=True) & Q(dropped_event__isnull=True)
        ).order_by('id')
        if emails:
            logging.info("se encontraron la siguente cantidad de emails pendientes")
            logging.info(emails.count())
            return emails
        else:
            return None

    @classmethod
    def get_delayed_emails_only_processed(self):
        emails = Email.objects.filter(
            Q(processed_event__isnull=False) &  Q(delivered_event__isnull=True) &
            Q(opened_event__isnull=True ) & Q(dropped_event__isnull=True) & 
            Q(bounce_event__isnull=True)).order_by('input_date')
        if emails:
            logging.info("se encontraron la siguente cantidad de emails pendientes")
            logging.info(emails.count())
            return emails
        else:
            return None

    @classmethod
    def get_emails_by_correo(self, date_from, date_to, correo, **kwargs):
        emails = Email.objects.filter(
            input_date__range=(date_from, date_to),
            correo=correo
        ).order_by('-input_date')
        query_total = emails.count()
        if kwargs['display_start'] is 0:
            emails = emails[kwargs['display_start']:kwargs['display_length']]
        else:
            emails = emails[kwargs['display_start']:kwargs['display_length']+kwargs['display_start']]
        if emails:
            query_length = emails.count()
        else:
            query_length = 0
        emails = serializers.serialize('json', emails)
        emails = json.loads(emails)
        data = []
        for e in emails:
            data.append(e['fields'])
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': data,
        }

    @classmethod
    def get_emails_by_correo_async(self, date_from, date_to, correo, **kwargs):
        emails = Email.objects.filter(
            input_date__range=(date_from, date_to),
            correo=correo).order_by('-input_date')
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_emails_by_dates_async(self, date_from, date_to, options, **kwargs):
        if date_from and date_to:
            emails = Email.objects.filter(
                input_date__range=(date_from, date_to))
            if emails:
                return emails
            else:
                return None

    @classmethod
    def get_sended_emails_by_dates_async(self, date_from, date_to, options='all'):
        if options == 'all':
            emails = Email.objects.filter(
                input_date__range=(date_from, date_to)).order_by('-input_date')
        else:
            emails = Email.objects.filter(
                input_date__range=(date_from, date_to),
                tipo_receptor=options).order_by('-input_date')
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_emails_by_folio(self, folio, **kwargs):
        if folio:
            emails = Email.objects.filter(
                numero_folio=folio
            ).order_by('-input_date')
            query_total = emails.count()
            if kwargs['display_start'] is 0:
                emails = emails[kwargs['display_start']:kwargs['display_length']]
            else:
                emails = emails[kwargs['display_start']:kwargs['display_length']+kwargs['display_start']]
            if emails:
                query_length = emails.count()
            else:
                query_length = 0
            emails = serializers.serialize('json', emails)
            emails = json.loads(emails)
            data = []
            for e in emails:
                data.append(e['fields'])
            return {
                'query_total': query_total,
                'query_length': query_length,
                'data': data,
            }

    @classmethod
    def get_emails_by_folio_async(self, folio, **kwargs):
        if folio:
            emails = Email.objects.filter(
                numero_folio=folio).order_by('-input_date')
            if emails:
                return emails
            else:
                return None

    @classmethod
    def get_emails_by_rut_receptor(self, date_from, date_to, rut, **kwargs):
        if date_from and date_to and rut:
            emails = Email.objects.filter(
                input_date__range=(date_from, date_to),
                rut_receptor=rut
            ).order_by('-input_date')
            query_total = emails.count()
            if kwargs['display_start'] is 0:
                emails = emails[kwargs['display_start']:kwargs['display_length']]
            else:
                emails = emails[kwargs['display_start']:kwargs['display_length']+kwargs['display_start']]
            if emails:
                query_length = emails.count()
            else:
                query_length = 0
            emails = serializers.serialize('json', emails)
            emails = json.loads(emails)
            data = []
            for e in emails:
                data.append(e['fields'])
            return {
                'query_total': query_total,
                'query_length': query_length,
                'data': data,
            }

    @classmethod
    def get_emails_by_rut_receptor_async(self, date_from, date_to, rut, **kwargs):
        if date_from and date_to and rut:
            emails = Email.objects.filter(
                input_date__range=(date_from, date_to),
                rut_receptor=rut).order_by('-input_date')
            if emails:
                return emails
            else:
                return None

    @classmethod
    def get_failure_emails_by_dates(self, date_from, date_to, **kwargs):
        emails = Email.objects.filter(
            Q(input_date__range=(date_from, date_to)),
            Q(bounce_event='bounce') | Q(dropped_event='dropped')
        ).order_by('-input_date')
        query_total = emails.count()
        if kwargs['display_start'] is 0:
            emails = emails[kwargs['display_start']:kwargs['display_length']]
        else:
            emails = emails[kwargs['display_start']:kwargs['display_length']+kwargs['display_start']]
        if emails:
            query_length = emails.count()
        else:
            query_length = 0
        emails = serializers.serialize('json', emails)
        emails = json.loads(emails)
        data = []
        for e in emails:
            data.append(e['fields'])
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': data,
        }

    @classmethod
    def get_failure_emails_by_dates_async(self, date_from, date_to, options, **kwargs):
        if date_from and date_to:
            emails = Email.objects.filter(
                Q(input_date__range=(date_from, date_to)),
                Q(bounce_event='bounce') | Q(dropped_event='dropped')
            ).order_by('-input_date')
            if emails:
                return emails
            else:
                return None

    @classmethod
    def get_emails_by_mount_and_dates(self, date_from, date_to, mount_from, mount_to, **kwargs):
        print kwargs
        emails = Email.objects.filter(
            input_date__range=(date_from, date_to),
            monto__range=(mount_from, mount_to),
        ).order_by('-input_date')
        query_total = emails.count()
        if kwargs['display_start'] is 0:
            emails = emails[kwargs['display_start']:kwargs['display_length']]
        else:
            emails = emails[kwargs['display_start']:kwargs['display_length']+kwargs['display_start']]
        if emails:
            query_length = emails.count()
        else:
            query_length = 0
        emails = serializers.serialize('json', emails)
        emails = json.loads(emails)
        data = []
        for e in emails:
            data.append(e['fields'])
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': data,
        }

    @classmethod
    def get_emails_by_mount_and_dates_async(self, date_from, date_to, mount_from, mount_to, **kwargs):
        emails = Email.objects.filter(
            input_date__range=(date_from, date_to),
            monto__range=(mount_from, mount_to)).order_by('-input_date')
        if emails:
            return emails
        else:
            return None
