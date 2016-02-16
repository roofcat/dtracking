# -*- coding: utf-8 -*-


import logging


from django.http import HttpResponse
from django.views.generic import TemplateView



class SendEmailEventToSoapWSView(TemplateView):

	def post(self, request, *args, **kwargs):
		logging.info("paso al TemplateView del Soap")
		return HttpResponse()


class SendEmailEventToRestWsView(TemplateView):

	def post(self, request, *args, **kwargs):
		logging.info("paso al TemplateView del Rest")
		return HttpResponse()
