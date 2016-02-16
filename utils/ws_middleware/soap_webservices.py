# -*- coding: utf-8 -*-


import logging
import suds


from configuraciones.models import SoapWebService
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
		conf = self.soap_conf
		if conf.url:
			if conf.con_autenticacion:
				pass
			if conf.solo_default:
				pass
			else:
				pass