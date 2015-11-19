# -*- coding: utf-8 -*-


from django.shortcuts import render


from rest_framework import viewsets


from .models import Empresa
from .serializers import EmpresaSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
	model = Empresa
	queryset = Empresa.objects.all()
	serializer_class = EmpresaSerializer
