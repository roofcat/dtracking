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
            email = Email.get_email_by_id(self.email_id)
            if email is not None:
                email = email.__dict__
                if self.soap_conf.con_autenticacion:
                    pass
                if self.soap_conf.solo_default:
                    data = dict()
                    params = (self.soap_conf.parametros_default).split(';')
                    for param in params:
                        data[param] = email[param]
                        client = SoapClient(self.soap_conf, self.event, data)
                        client.web_service_load()
                else:
                    pass
            else:
                logging.error("Email id no corresponde")
        else:
            logging.error('No hay url soap ws configurada')


class SoapClient(object):

    def __init__(self, conf, event, data):
        self.conf = conf
        self.event = event
        self.data = data

    def web_service_load(self):
        try:
            logging.info(self.conf.url)
            client = Client(self.conf.url)
            logging.info(self.data)
        except Exception, e:
            logging.error(e)
            return None
