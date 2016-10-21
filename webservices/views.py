# -*- coding: utf-8 -*-


import logging

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from utils.ws_middleware import SoapMiddleware


class SendEmailEventToSoapWSView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SendEmailEventToSoapWSView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logging.info("paso al TemplateView del Soap")
        email_id = request.POST.get('email_id')
        event = request.POST.get('event')
        soap_ws = SoapMiddleware(email_id, event)
        soap_ws.execute()
        return HttpResponse()


class SendEmailEventToRestWsView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SendEmailEventToRestWsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logging.info("paso al TemplateView del Rest")
        return HttpResponse()
