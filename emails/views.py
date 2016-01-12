# -*- coding: utf-8 -*-


from datetime import date, timedelta
import json
import logging


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET


from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import Email
from .serializers import EmailDteInputSerializer
from configuraciones.models import EliminacionHistorico
from utils.queues import input_queue
from utils.sendgrid_client import EmailClient


class EmailDteInputView(APIView):
    serializer_class = EmailDteInputSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id=None, format=None):
        if id is not None:
            email = get_object_or_404(Email, pk=id)
            response = self.serializer_class(email, many=False)
        else:
            emails = Email.objects.all()
            response = self.serializer_class(emails, many=True)
        return Response(response.data)

    def post(self, request, format=None):
        email = self.serializer_class(data=request.data)
        if email.is_valid():
            email.save()
            logging.info(email.data)
            input_queue(email.data['id'])
            #email_client = EmailClient()
            #email_client.enviar_correo_dte(email.data['id'])
            return Response({'status': 200})
        else:
            logging.error(email.errors)
            return Response(email.errors)


@csrf_exempt
@require_POST
def queue_send_email(request):
    if request.method == 'POST':
        logging.info("entrando a la cola")
        logging.info(request.body)
        try:
            email_id = request.POST.get('email_id')
            email_id = int(email_id, base=10)
            email_client = EmailClient()
            email_client.enviar_correo_dte(email_id)
            return HttpResponse()
        except Exception, e:
            logging.error(e)

@csrf_exempt
@require_GET
def cron_clean_emails_history(request):
    ''' Método que si tiene habilitada la opción de eliminar correos antiguos
        antiguos (parametrizado en app configuraciones) lista los correos 
        desde el numero de meses máximo a retener en la DB.
    '''
    if request.method == 'GET':
        config = EliminacionHistorico.get_configuration()[0]
        if config.activo == True:
            if config.dias_a_eliminar is not None:
                try:
                    today = date.today()
                    days = timedelta(days=config.dias_a_eliminar)
                    date_to_delete = today - days
                    emails = Email.delete_old_emails_by_date(date_to_delete)
                except Exception, e:
                    logging.error(e)
                    return HttpResponse(e)
    return HttpResponse()

@csrf_exempt
@require_GET
def cron_send_delayed_email(request):
    if request.method == 'GET':
        logging.info("entrando a la cola de reenvio de correos")
        logging.info(request.body)
        emails = Email.get_delayed_emails()
        if emails is not None:
            for email in emails:
                input_queue(email.id)
        return HttpResponse()

@csrf_exempt
@require_GET
def cron_send_delayed_processed_email(request):
    if request.method == 'GET':
        logging.info("entrando a la cola de reenvio de correos")
        logging.info(request.body)
        emails = Email.get_delayed_emails_only_processed()
        if emails is not None:
            for email in emails:
                input_queue(email.id)
        return HttpResponse()
