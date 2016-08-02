# -*- coding: utf-8 -*-


from django.db import models


class Holding(models.Model):
	nombre = models.CharField(max_length=200, unique=True, db_index=True)

	def __unicode__(self):
		return u'{0}'.format(self.nombre)


class Empresa(models.Model):
	holding = models.ForeignKey(Holding, null=True)
	rut = models.CharField(primary_key=True, unique=True, max_length=20)
	empresa = models.CharField(max_length=200)

	def __unicode__(self):
		return u'{0}'.format(self.empresa)
