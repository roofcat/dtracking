# -*- coding: utf-8 -*-


from django.db import models


class Empresa(models.Model):
	rut = models.CharField(primary_key=True, unique=True, max_length=20)
	empresa = models.CharField(max_length=200)

	def __unicode__(self):
		return u'{0}'.format(self.empresa)
