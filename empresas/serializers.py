# -*- coding: utf-8 -*-


from rest_framework.serializers import ModelSerializer


from .models import Empresa


class EmpresaSerializer(ModelSerializer):

	class Meta:
		model = Empresa
		fields = ('rut', 'empresa',)
