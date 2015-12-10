# -*- coding: utf-8 -*-


from google.appengine.api import taskqueue
import json
import logging


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import Email
from .serializers import EmailDteInputSerializer
from sendgrid_manager.sendgrid_client import EmailClient


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
            context = {
                "email_id": email.data['id'],
            }
            q = taskqueue.Queue("InputQueue")
            t = taskqueue.Task(url="/api/input/inputqueue/", params=context)
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


class EmailViewSet(ModelViewSet):
    model = Email
    queryset = Email.objects.all()
    serializer_class = EmailDteInputSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        return super(EmailViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logging.info("paso el post ahora mandarlo en cola")
        logging.info(request.data)
        return super(EmailViewSet, self).create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(EmailViewSet, self).create(request, *args, **kwargs)
