# -*- coding: utf-8 -*-


import json
import logging


from rest_framework import viewsets, permissions


from .models import Email
from .serializers import EmailSerializer


class EmailViewSet(viewsets.ModelViewSet):
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
