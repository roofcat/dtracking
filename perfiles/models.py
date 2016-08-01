# -*- coding: utf-8 -*-


from __future__ import unicode_literals


import logging


from django.db import models
from django.contrib.auth.models import User


from empresas.models import Empresa


class Perfil(models.Model):
	usuario = models.ForeignKey(User)
	empresas = models.ManyToManyField(Empresa)

	def __unicode__(self):
		return u'{0}'.format(self.empresas, self.usuario)

	@classmethod
	def get_perfil(self, user):
		try:
			return Perfil.objects.get(usuario=user)
		except Exception, e:
			logging.error(e)
