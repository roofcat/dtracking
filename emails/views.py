# -*- coding: utf-8 -*-


from datetime import date, timedelta
import cloudstorage
import json
import logging


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import Email
from .serializers import EmailDteInputSerializer
from configuraciones.models import EliminacionHistorico
from empresas.models import Empresa
from utils.queues import input_queue
from utils.sendgrid_client import EmailClient


class EmailDteInputView(APIView):
    ''' Vista encargada de recibir los request vía json post
        para crear nuevos email y enviarlos por correo
    '''
    serializer_class = EmailDteInputSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id=None, format=None):
        if id is not None:
            email = get_object_or_404(Email, pk=id)
            response = self.serializer_class(email, many=False)
        else:
            emails = Email.objects.all().order_by('-id')[:5]
            response = self.serializer_class(emails, many=True)
        return Response(response.data)

    def post(self, request, format=None):
        email = self.serializer_class(data=request.data)
        if email.is_valid():
            email.save()
            logging.info(email.data)
            input_queue(email.data['id'], email.data['empresa'])
            #email_client = EmailClient()
            #email_client.enviar_correo_dte(email.data['id'])
            return Response({'status': 200})
        else:
            logging.error(email.errors)
            return Response(email.errors)


class QueueSendEmailView(TemplateView):
    ''' Vista encargada de recibir la cola de solicitudes de envío de
        correos y envía los correo con sus adjuntos
    '''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(QueueSendEmailView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logging.info("Entrando a la cola de envío de emails.")
        logging.info(request.body)
        try:
            # recibir parametros de la cola
            email_id = request.POST.get('email_id')
            email_id = int(email_id, base=10)
            empresa_id = request.POST.get('empresa_id')
            # enviar correo
            email_client = EmailClient(empresa_id)
            email_client.enviar_correo_dte(email_id)
            return HttpResponse()
        except Exception, e:
            logging.error(e)


class CronCleanEmailsHistoryView(TemplateView):
    ''' Método que si tiene habilitada la opción de eliminar correos antiguos
        antiguos (parametrizado en app configuraciones) lista los correos
        desde el numero de meses máximo a retener en la DB.
    '''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CronCleanEmailsHistoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Listar todas las configuraciones activas
        active_configs = EliminacionHistorico.objects.filter(activo=True)

        # Recorrer listado
        for config in active_configs:
            if config.activo == True:
                if config.dias_a_eliminar is not None:
                    try:
                        # resta la fecha de hoy con los días a eliminar
                        today = date.today()
                        days = timedelta(days=config.dias_a_eliminar)
                        date_to_delete = today - days
                        # listar las empresas al holding que pertenece la conf actual
                        empresas = Empresa.objects.filter(holding=config.holding)
                        for empresa in empresas:
                            # enviar la petición para borrar
                            emails = Email.delete_old_emails_by_date(date_to_delete, empresa)
                    except Exception, e:
                        logging.error(e)
                        return HttpResponse(e)
        return HttpResponse()


class CronSendDelayedEmailView(TemplateView):
    ''' Evalúa los correos que no se han podido enviar,
        los correos que caen en este proceso son aquellos que son
        ingresados vía json post en el servicio rest publicado
    '''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CronSendDelayedEmailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logging.info("entrando a la cola de reenvio de correos")
        logging.info(request.body)
        emails = Email.get_delayed_emails()
        if emails is not None:
            for email in emails:
                input_queue(email.id)
        return HttpResponse()


class CronSendDelayedProcessedEmailView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CronSendDelayedProcessedEmailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logging.info("entrando a la cola de reenvio de correos")
        logging.info(request.body)
        emails = Email.get_delayed_emails_only_processed()
        if emails is not None:
            for email in emails:
                input_queue(email.id)
        return HttpResponse()


class DeleteEmailFileView(TemplateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteEmailFileView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logging.info("entrando a la cola de eliminación de archivos")
        logging.info(request.body)
        file_url = request.POST.get('file_url')
        cloudstorage.delete(file_url)
        return HttpResponse()
