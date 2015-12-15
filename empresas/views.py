# -*- coding: utf-8 -*-


from rest_framework.viewsets import ModelViewSet


from .models import Empresa
from .serializers import EmpresaSerializer


class EmpresaViewSet(ModelViewSet):
	model = Empresa
	queryset = Empresa.objects.all()
	serializer_class = EmpresaSerializer
