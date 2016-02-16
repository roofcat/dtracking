# -*- coding: utf-8 -*-


from configuraciones.models import SoapWebService
from utils.queues import soap_ws_queue


class SoapMiddleware(object):

	def __init__(self, email_id, event):
		self.email_id = email_id
		self.event = event
		self.soap_conf = SoapWebService.get_ws_conf()

	def evaluate(self):
		if self.soap_conf.count() > 0:
			context = {
				'email_id': self.email_id,
				'event': self.event,
			}
			soap_ws_queue(context)
