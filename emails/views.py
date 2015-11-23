# -*- coding: utf-8 -*-


import json
import logging


from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import Email
from .serializers import EmailSerializer


class SaludoView(APIView):
    serializer_class = EmailSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        emails = Email.objects.all()
        response = self.serializer_class(emails, many=True)
        return Response(response.data)

saludo_view = SaludoView.as_view()


class EmailViewSet(ModelViewSet):
    model = Email
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
    	return super(EmailViewSet, self).list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logging.error("paso el post ahora mandarlo en cola")
		logging.error(request)
		return request
