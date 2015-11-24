# -*- coding: utf-8 -*-


import json
import logging


from django.shortcuts import get_object_or_404


from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import Email
from .serializers import EmailSerializer


class SaludoView(APIView):
    serializer_class = EmailSerializer
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
            logging.info(email.data['id'])
            return Response(email.data)
        else:
            logging.error(email.errors)
            return Response(email.errors)

saludo_view = SaludoView.as_view()


class EmailViewSet(ModelViewSet):
    model = Email
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        return super(EmailViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logging.info("paso el post ahora mandarlo en cola")
        logging.info(request.data)
        return super(EmailViewSet, self).create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(EmailViewSet, self).create(request, *args, **kwargs)
