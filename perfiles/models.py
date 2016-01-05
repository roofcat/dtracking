# -*- coding: utf-8 -*-


from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import User


from empresas.models import Empresa


class Perfil(models.Model):
	usuario = models.ForeignKey(User)
	es_admin = models.BooleanField(default=False)
	empresa = models.ManyToManyField(Empresa)

	def __unicode__(self):
		return u'{0}'.format(self.usuario)
