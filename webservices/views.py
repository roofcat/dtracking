# -*- coding: utf-8 -*-


import logging


from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView



class SendEmailEventToSoapWSView(TemplateView):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(SendEmailEventToSoapWSView, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logging.info("paso al TemplateView del Soap")
		return HttpResponse()


class SendEmailEventToRestWsView(TemplateView):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(SendEmailEventToRestWsView, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logging.info("paso al TemplateView del Rest")
		return HttpResponse()
