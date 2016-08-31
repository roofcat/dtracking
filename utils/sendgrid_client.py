# -*- coding: utf-8 -*-


import logging
from sendgrid import SendGridClient, Mail


from django.contrib.auth.models import User


from configuraciones.models import SendgridConf, TemplateReporte
from emails.models import Email
from utils.generics import get_file_name_from_storage


class EmailClient(object):

    def __init__(self, empresa_id):
        self.empresa_id = empresa_id
        # llamar las configuraciones en la DB
        self.email_config = SendgridConf.get_sg_config(self.empresa_id)
        # crear los atributos de la instancia de SendGrid
        self.sg = SendGridClient(self.email_config.api_key)
        self.message = Mail()
        self.message.set_from(self.email_config.asunto_email_dte)
        self.message.set_from_name(self.email_config.nombre_email_dte)

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
            'tipo_dte': correo.tipo_dte.id_documento,
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
        logging.info(correo)
        if correo.xml:
            self.message.add_attachment_stream(
                get_file_name_from_storage(correo.xml.name),
                correo.xml.file.read())
        if correo.pdf:
            self.message.add_attachment_stream(
                get_file_name_from_storage(correo.pdf.name),
                correo.pdf.file.read())
        if correo.adjunto1:
            self.message.add_attachment_stream(
                get_file_name_from_storage(correo.adjunto1.name),
                correo.adjunto1.file.read())
        self.message.set_unique_args(unique_args)
        # enviando el mail
        status, msg = self.sg.send(self.message)
        # imprimiendo respuesta
        logging.info(status)
        logging.info(msg)

    def send_report_to_user_with_attach(self, user_email, report):
        # parametros de correo reporte
        self.message.set_from(self.email_config.asunto_email_reporte)
        self.message.set_from_name(self.email_config.nombre_email_reporte)
        # buscar usuario
        template_config = TemplateReporte.get_configuration(self.empresa_id)
        # preparar template del correo reporte
        user = User.objects.get(email=user_email)
        html = str(template_config.template_html).format(
            user_name=user.first_name)
        # valores de envío
        self.message.add_to(user_email)
        self.message.add_to_name(user.first_name)
        self.message.set_subject(template_config.asunto_reporte)
        self.message.set_html(html)
        # adjuntar excel si esta
        if report['report']:
            self.message.add_attachment_stream(
                report['name'], report['report'])
        # enviando el correo
        status, msg = self.sg.send(self.message)
        # imprimiendo respuesta
        logging.info(status)
        logging.info(msg)
