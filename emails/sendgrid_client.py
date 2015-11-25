# -*- coding: utf-8 -*-


import logging


from sendgrid import SendGridClient, Mail


from .models import Email
from configuraciones.models import SendgridConf


email_config = SendgridConf.objects.all()[:1].get()


class EmailClient(object):

    def __init__(self):
        self.sg = SendGridClient(email_config.api_key)
        self.message = Mail()
        self.message.set_from(email_config.asunto_email_dte)
        self.message.set_from_name(email_config.nombre_email_dte)

    def enviar_correo_dte(self, id):
    	# cargar el objecto de id
    	correo = Email.objects.get(pk=id)
        # valores de envío
        self.message.add_to(correo.correo)
        self.message.add_to_name(correo.nombre_cliente)
        self.message.set_subject(correo.asunto)
        self.message.set_html(correo.html)
        # valores personalizados
        unique_args = {
        	'email_id': correo.id,
            'empresa': correo.empresa.rut,
            'rut_receptor': correo.rut_receptor,
            'rut_emisor': correo.rut_emisor,
            'tipo_envio': correo.tipo_envio,
            'tipo_dte': correo.tipo_dte,
            'numero_folio': correo.numero_folio,
            'resolucion_receptor': correo.resolucion_receptor,
            'resolucion_emisor': correo.resolucion_emisor,
            'monto': correo.monto,
            'fecha_emision': correo.fecha_emision,
            'fecha_recepcion': correo.fecha_recepcion,
            'estado_documento': correo.estado_documento,
            'tipo_operacion': correo.tipo_operacion,
            'tipo_receptor': correo.tipo_receptor,
        }
        if correo.adjunto1:
            self.message.add_attachment_stream(correo.name, correo)
        self.message.set_unique_args(unique_args)
        # enviando el mail
        status, msg = self.sg.send(self.message)
        # imprimiendo respuesta
        logging.info(status)
        logging.info(msg)
