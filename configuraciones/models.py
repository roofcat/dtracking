# -*- coding: utf-8 -*-


from django.db import models


class SendgridConf(models.Model):
	api_key = models.CharField(max_length=200, db_index=True)
	api_user = models.CharField(max_length=200, db_index=True)
	api_pass = models.CharField(max_length=200, db_index=True)
	asunto_email_dte = models.EmailField(max_length=240, db_index=True)
	nombre_email_dte = models.CharField(max_length=200, db_index=True)
	asunto_email_reporte = models.EmailField(max_length=240, db_index=True)
	nombre_email_reporte = models.CharField(max_length=240, db_index=True)

	def __unicode__(self):
		return u'{0}'.format(self.api_user)


class TemplateReporte(models.Model):
	reporte_url = models.URLField(max_length=200, db_index=True, blank=True)
	asunto_reporte = models.CharField(max_length=240, db_index=True)
	template_html = models.TextField()

	def __unicode__(self):
		return u'{0}'.format(self.reporte_url)


class EliminacionHistorico(models.Model):
	activo = models.BooleanField(default=False)
	dias_a_eliminar = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return u'{0} - {1}'.format(self.activo, self.dias_a_eliminar)

	@classmethod
	def get_configuration(self):
		conf = EliminacionHistorico.objects.all()[:1]
		if conf is not None:
			return conf
		else:
			return None
