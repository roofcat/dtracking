# -*- coding: utf-8 -*-


import logging
from suds.client import Client


from configuraciones.models import SoapWebService
from emails.models import Email
from utils.queues import soap_ws_queue


class SoapMiddleware(object):

    def __init__(self, email_id, event):
        self.email_id = email_id
        self.event = event
        self.soap_conf = SoapWebService.get_ws_conf()

    def evaluate(self):
        if self.soap_conf is not None:
            context = {
                'email_id': self.email_id,
                'event': self.event,
            }
            soap_ws_queue(context)

    def execute(self):
        if self.soap_conf.url:
            client = Client(self.soap_conf.url)
            email = Email.get_email_by_id(self.email_id)
            documento = None

            if email is not None:
                email = email.__dict__
                if self.soap_conf.con_autenticacion:
                    pass

                if self.soap_conf.con_objeto_documento:
                    documento = client.factory.create(self.soap_conf.nombre_objeto_documento)
                    doc_attr = (self.soap_conf.parametros_objeto_documento).split(';')
                    doc_field = (self.soap_conf.campos_objeto_documento).split(';')
                    for att, field in doc_attr, doc_field:
                        documento[att] = email[field]
                    print documento

                if self.soap_conf.solo_default:
                    data = dict()
                    params = (self.soap_conf.parametros_default).split(';')
                    for param in params:
                        data[param] = email[param]
                    if documento is not None:
                        data[self.soap_conf.nombre_objeto_documento] = documento
                    client = getattr(client.service, self.soap_conf.metodo_default)
                    print client(**data)
                else:
                    if self.event == 'processed':
                        pass
                    elif self.event == 'delivered':
                        pass
                    elif self.event == 'open':
                        pass
                    elif self.event == 'dropped':
                        pass
                    elif self.event == 'bounce':
                        pass
            else:
                logging.error("Email id no corresponde")
        else:
            logging.error('No hay url soap ws configurada')

    def __objeto_documento():
        pass
