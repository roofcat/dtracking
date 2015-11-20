# -*- coding: utf-8 -*-


import json
import logging


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


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


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard/index.html')


@login_required(login_url='/login/')
def customsearch(request):
    return render(request, 'customsearch/index.html')
