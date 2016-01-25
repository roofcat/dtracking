# -*- coding: utf-8 -*-


from datetime import datetime
import calendar
import cloudstorage
import json
import logging


from django.db import models
from django.db.models import Count, Q
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict


from empresas.models import Empresa
from tipodocumentos.models import TipoDocumento
from utils.generics import timestamp_to_date


TIPOS_RECEPTORES = (
    ('electronico', 'electronico'),
    ('manual', 'manual'),
    ('ambos', 'ambos'),
)
TIPOS_ENVIOS = (
    ('aceptacion', 'aceptacion'),
    ('envio dte', 'envio dte'),
    ('notificacion', 'notificacion'),
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


class FileQuerySet(models.QuerySet):
    """ Clase encargada de eliminar los adjuntos en casos de
        DELETE's masivos
    """

    def delete(self, *args, **kwargs):
        try:
            for obj in self:
                logging.info("borrando adjunto de GCS")
                logging.info(obj)
                if obj.adjunto1 == '' or obj.adjunto1 is None:
                    pass
                else:
                    cloudstorage.delete(obj.adjunto1.name)
            super(FileQuerySet, self).delete(*args, **kwargs)
        except Exception, e:
            logging.error(e)


class Email(models.Model):
    # campos basicos
    input_date = models.DateField(auto_now_add=True, db_index=True)
    # campos dte
    empresa = models.ForeignKey(Empresa)
    rut_receptor = models.CharField(max_length=20, db_index=True)
    rut_emisor = models.CharField(max_length=20, db_index=True)
    tipo_envio = models.CharField(max_length=20,
                                  choices=TIPOS_ENVIOS,
                                  db_index=True)
    tipo_dte = models.ForeignKey(TipoDocumento)
    numero_folio = models.BigIntegerField(db_index=True)
    resolucion_receptor = models.IntegerField(null=True, blank=True)
    resolucion_emisor = models.IntegerField(null=True, blank=True)
    monto = models.BigIntegerField(default=0, db_index=True)
    fecha_emision = models.BigIntegerField(null=True, blank=True)
    fecha_recepcion = models.BigIntegerField(null=True, blank=True)
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
    id_envio = models.IntegerField(blank=True, null=True)
    # campos correo
    nombre_cliente = models.CharField(max_length=200)
    correo = models.EmailField(max_length=250, db_index=True)
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

    # metodos manager al objects
    objects = FileQuerySet.as_manager()

    def __unicode__(self):
        return u"{0} - {1}".format(self.correo, self.numero_folio)

    def delete(self, *args, **kwargs):
        try:
            cloudstorage.delete(self.adjunto1.name)
            super(Email, self).delete(*args, **kwargs)
        except cloudstorage.NotFoundError, e:
            logging.error(e)

    # funcion utilizada desde el webhook rest
    @classmethod
    def get_email_by_id(self, email_id):
        try:
            email = Email.objects.get(pk=email_id)
            logging.info("Email Existe")
        except Email.DoesNotExist:
            logging.error("Email.DoesNotExist")
            email = None
        return email

    # funcion DRY para webhook api
    @classmethod
    def set_default_fields(self, body):
        empresa_id = str(body['empresa']).decode('utf-8')
        rut_receptor = str(body['rut_receptor']).decode('utf-8')
        rut_emisor = str(body['rut_emisor']).decode('utf-8')
        tipo_envio = str(body['tipo_envio']).decode('utf-8')
        tipo_dte_id = body['tipo_dte']
        numero_folio = body['numero_folio']
        resolucion_receptor = body['resolucion_receptor']
        if resolucion_receptor == '' or None:
            resolucion_receptor = 0
        resolucion_emisor = body['resolucion_emisor']
        monto = body['monto']
        fecha_emision = body['fecha_emision']
        if fecha_emision == '' or None:
            fecha_emision = 0
        fecha_recepcion = body['fecha_recepcion']
        if fecha_recepcion == '' or None:
            fecha_recepcion = 0
        estado_documento = str(body['estado_documento']).decode('utf-8')
        tipo_operacion = str(body['tipo_operacion']).decode('utf-8')
        tipo_receptor = str(body['tipo_receptor']).decode('utf-8')
        nombre_cliente = str(body['nombre_cliente']).decode('utf-8')
        correo = str(body['email']).decode('utf-8')

        email = Email.objects.create(
            empresa_id=empresa_id,
            rut_receptor=rut_receptor,
            rut_emisor=rut_emisor,
            tipo_envio=tipo_envio,
            tipo_dte_id=tipo_dte_id,
            numero_folio=numero_folio,
            resolucion_receptor=resolucion_receptor,
            resolucion_emisor=resolucion_emisor,
            monto=monto,
            fecha_emision=fecha_emision,
            fecha_recepcion=fecha_recepcion,
            estado_documento=estado_documento,
            tipo_operacion=tipo_operacion,
            tipo_receptor=tipo_receptor,
            nombre_cliente=nombre_cliente,
            correo=correo
        )
        return email

    # funcion utilizada desde el webhook api
    @classmethod
    def get_email(self, correo, numero_folio, tipo_dte, rut_emisor, resolucion_emisor):
        if isinstance(numero_folio, (str, basestring)):
            numero_folio = int(numero_folio, base=10)
        if isinstance(tipo_dte, (str, basestring)):
            tipo_dte = int(tipo_dte, base=10)
        if isinstance(resolucion_emisor, (str, basestring)):
            resolucion_emisor = int(resolucion_emisor, base=10)
        """
        try:
            email = Email.objects.get(
                correo=correo,
                numero_folio=numero_folio,
                tipo_dte_id=tipo_dte,
                rut_emisor=rut_emisor,
                resolucion_emisor=resolucion_emisor,
            )
            return email
        except Email.DoesNotExist:
            return None
        """
        try:
            email = Email.objects.filter(
                correo=correo,
                numero_folio=numero_folio,
                tipo_dte_id=tipo_dte,
                rut_emisor=rut_emisor,
                resolucion_emisor=resolucion_emisor,
            )
            logging.info(email)
            logging.info(len(email))
            logging.info(email.query)
            if email:
                return email[0]
            else:
                return None
        except Exception, e:
            logging.error(e)
            return None

    # MÉTODOS DE CONSULTAS (para no repetir código)
    @classmethod
    def get_statistics_count_by_dates(self, date_from, date_to, empresa='all', options='all'):
        # Primero validar si se debe filtrar o no por empresa
        if empresa == 'all':
            # si se consulta por todas las empresas se evalúa el tipo de receptor
            if options == 'all':
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
            else:
                count_total = Email.objects.filter(
                    input_date__range=(date_from, date_to), 
                    tipo_receptor=options).count()
                count_processed = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    processed_event='processed',
                    tipo_receptor=options).count()
                count_delivered = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    delivered_event='delivered',
                    tipo_receptor=options).count()
                count_opened = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    opened_event='open',
                    tipo_receptor=options).count()
                count_dropped = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    dropped_event='dropped',
                    tipo_receptor=options).count()
                count_bounce = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    bounce_event='bounce',
                    tipo_receptor=options).count()
        else:
            if options == 'all':
                count_total = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    empresa=empresa).count()
                count_processed = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    processed_event='processed',
                    empresa=empresa).count()
                count_delivered = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    delivered_event='delivered',
                    empresa=empresa).count()
                count_opened = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    opened_event='open',
                    empresa=empresa).count()
                count_dropped = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    dropped_event='dropped',
                    empresa=empresa).count()
                count_bounce = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    bounce_event='bounce',
                    empresa=empresa).count()
            else:
                count_total = Email.objects.filter(
                    input_date__range=(date_from, date_to), 
                    tipo_receptor=options,
                    empresa=empresa).count()
                count_processed = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    processed_event='processed',
                    tipo_receptor=options,
                    empresa=empresa).count()
                count_delivered = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    delivered_event='delivered',
                    tipo_receptor=options,
                    empresa=empresa).count()
                count_opened = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    opened_event='open',
                    tipo_receptor=options,
                    empresa=empresa).count()
                count_dropped = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    dropped_event='dropped',
                    tipo_receptor=options,
                    empresa=empresa).count()
                count_bounce = Email.objects.filter(
                    input_date__range=(date_from, date_to),
                    bounce_event='bounce',
                    tipo_receptor=options,
                    empresa=empresa).count()
        return {
            'total': count_total,
            'processed': count_processed,
            'delivered': count_delivered,
            'opened': count_opened,
            'dropped': count_dropped,
            'bounced': count_bounce,
        }

    @classmethod
    def get_statistics_range_by_dates(self, date_from, date_to, empresa='all', options='all'):
        if empresa == 'all':
            if options == 'all':
                emails = Email.objects.filter(input_date__range=(
                    date_from, date_to)).values('input_date').annotate(
                    total=Count('input_date'), processed=Count('processed_event'),
                    delivered=Count('delivered_event'), opened=Count('opened_event'),
                    dropped=Count('dropped_event'), bounced=Count('bounce_event')
                ).order_by('input_date')
            else:
                emails = Email.objects.filter(input_date__range=(
                    date_from, date_to), tipo_receptor=options).values('input_date').annotate(
                    total=Count('input_date'), processed=Count('processed_event'),
                    delivered=Count('delivered_event'), opened=Count('opened_event'),
                    dropped=Count('dropped_event'), bounced=Count('bounce_event')
                ).order_by('input_date')
        else:
            if options == 'all':
                emails = Email.objects.filter(input_date__range=(
                    date_from, date_to), empresa=empresa).values('input_date').annotate(
                    total=Count('input_date'), processed=Count('processed_event'),
                    delivered=Count('delivered_event'), opened=Count('opened_event'),
                    dropped=Count('dropped_event'), bounced=Count('bounce_event')
                ).order_by('input_date')
            else:
                emails = Email.objects.filter(input_date__range=(
                    date_from, date_to), tipo_receptor=options, empresa=empresa).values('input_date').annotate(
                    total=Count('input_date'), processed=Count('processed_event'),
                    delivered=Count('delivered_event'), opened=Count('opened_event'),
                    dropped=Count('dropped_event'), bounced=Count('bounce_event')
                ).order_by('input_date')
        data = []
        for email in emails:
            email = json.dumps(email, cls=DjangoJSONEncoder)
            data.append(json.loads(email))
        return data

    @classmethod
    def delete_old_emails_by_date(self, date_to_delete):
        try:
            emails = Email.objects.filter(input_date__lt=date_to_delete).delete()
        except Exception, e:
            logging.error(e)

    @classmethod
    def get_emails_by_dynamic_query(self, date_from, date_to, empresa, correo, 
                                    folio, rut, mount_from, mount_to, fallidos,
                                    display_start, display_length):
        if folio is not None:
            if empresa is None:
                print "query de folio sin empresa"
                emails = Email.objects.filter(
                    numero_folio=folio).order_by('-input_date')
            else:
                print "query de folio con empresa"
                emails = Email.objects.filter(
                    empresa=empresa, numero_folio=folio
                ).order_by('-input_date')
        elif fallidos is True:
            print "query de fallidos"
            emails = Email.objects.filter(
                Q(input_date__range=(date_from, date_to)),
                Q(bounce_event='bounce') | Q(dropped_event='dropped')
            ).order_by('-input_date')
        else:
            params = {}
            print "query dinamica"
            if date_from and date_to:
                params['input_date__range'] = (date_from, date_to)
            if empresa is not None:
                print "con empresa"
                params['empresa'] = empresa
            if correo is not None:
                print "con correo"
                params['correo'] = correo
            if rut is not None:
                print "con rut receptor"
                params['rut_receptor'] = rut
            if mount_from is not None and mount_to is not None:
                print "con montos"
                params['monto__range'] = (mount_from, mount_to)
            emails = Email.objects.filter(**params).order_by('-input_date')
        # imprimir consulta
        print "query"
        print emails.query
        # despues de consultar paginar y preparar retorno de emails
        query_total = emails.count()
        print query_total
        if display_start is 0:
            emails = emails[display_start:display_length]
        else:
            emails = emails[display_start:display_length + display_start]
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
        display_start
        display_length

    @classmethod
    def get_emails_by_dynamic_query_async(self, date_from, date_to, empresa, correo, 
                                        folio, rut, mount_from, mount_to, fallidos):

        date_from = timestamp_to_date(date_from)
        date_to = timestamp_to_date(date_to)
        if folio is not None:
            if empresa is None:
                print "query de folio sin empresa"
                emails = Email.objects.filter(
                    numero_folio=folio).order_by('-input_date')
            else:
                print "query de folio con empresa"
                emails = Email.objects.filter(
                    empresa=empresa, numero_folio=folio
                ).order_by('-input_date')
        elif fallidos is True:
            print "query de fallidos"
            emails = Email.objects.filter(
                Q(input_date__range=(date_from, date_to)),
                Q(bounce_event='bounce') | Q(dropped_event='dropped')
            ).order_by('-input_date')
        else:
            params = {}
            print "query dinamica"
            if date_from and date_to:
                params['input_date__range'] = (date_from, date_to)
            if empresa is not None:
                print "con empresa"
                params['empresa'] = empresa
            if correo is not None:
                print "con correo"
                params['correo'] = correo
            if rut is not None:
                print "con rut receptor"
                params['rut_receptor'] = rut
            if mount_from is not None and mount_to is not None:
                print "con montos"
                params['monto__range'] = (mount_from, mount_to)
            emails = Email.objects.filter(**params).order_by('-input_date')
        # imprimir consulta
        print "query"
        print emails.query
        # despues de consultar paginar y preparar retorno de emails
        query_total = emails.count()
        print query_total
        # retornar emails
        if emails:
            return emails
        else:
            return None

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
            correo=correo).order_by('-input_date')[:20000]
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_emails_by_dates_async(self, date_from, date_to, empresa, options='all'):
        params = {}
        params['input_date__range'] = (date_from, date_to)
        if empresa != 'all':
            params['empresa'] = empresa
        if options != 'all':
            params['tipo_receptor'] = options
        emails = Email.objects.filter(**params).order_by('input_date')[:20000]
        if emails:
            return emails
        else:
            return None

    @classmethod
    def get_sended_emails_by_dates_async(self, date_from, date_to, empresa, options='all'):
        params = {}
        params['input_date__range'] = (date_from, date_to)
        if empresa != 'all':
            params['empresa'] = empresa
        if options != 'all':
            params['tipo_receptor'] = options
        emails = Email.objects.filter(**params).order_by('input_date')[:20000]
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
                numero_folio=folio).order_by('-input_date')[:20000]
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
                rut_receptor=rut).order_by('-input_date')[:20000]
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
    def get_failure_emails_by_dates_async(self, date_from, date_to, empresa, options):
        if empresa == 'all':
            if options == 'all':
                emails = Email.objects.filter(
                    Q(input_date__range=(date_from, date_to)),
                    Q(bounce_event='bounce') | Q(dropped_event='dropped')
                )
            else:
                emails = Email.objects.filter(
                    Q(input_date__range=(date_from, date_to)),
                    Q(tipo_receptor=options),
                    Q(bounce_event='bounce') | Q(dropped_event='dropped')
                )
        else:
            if options == 'all':
                emails = Email.objects.filter(
                    Q(input_date__range=(date_from, date_to)),
                    Q(empresa=empresa),
                    Q(bounce_event='bounce') | Q(dropped_event='dropped')
                )
            else:
                emails = Email.objects.filter(
                    Q(input_date__range=(date_from, date_to)),
                    Q(tipo_receptor=options), Q(empresa=empresa),
                    Q(bounce_event='bounce') | Q(dropped_event='dropped')
                )
        emails = emails.order_by('input_date')[:20000]
        print emails.query
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
            monto__range=(mount_from, mount_to)).order_by('-input_date')[:20000]
        if emails:
            return emails
        else:
            return None
