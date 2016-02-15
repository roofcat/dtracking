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


class WebServicesWebhooks(models.Model):
    url = models.URLField(max_length=255)
    con_autenticacion = models.BooleanField(default=False)
    usuario_autenticacion = models.CharField(max_length=200, null=True)
    clave_autenticacion = models.CharField(max_length=200, null=True)
    solo_default = models.BooleanField(default=False)
    metodo_default = models.CharField(max_length=200)
    parametros_default = models.CharField(max_length=255, blank=True,
                                          help_text='Lista de parametros ordenados \
                                          por posición en el metodo del Web Service \
                                          separado por ; sin espacios ejemplo: \
										  "rut_emisor;numero_folio;input_date"')
    con_procesado = models.BooleanField(default=False)
    metodo_procesado = models.CharField(max_length=200, null=True)
    parametros_procesado = models.CharField(max_length=255, null=True)
    con_enviado = models.BooleanField(default=False)
    metodo_enviado = models.CharField(max_length=200, null=True)
    parametros_eviado = models.CharField(max_length=255, null=True)
    con_leido = models.BooleanField(default=False)
    metodo_leido = models.CharField(max_length=200, null=True)
    parametros_leido = models.CharField(max_length=255, null=True)
    con_rebotado = models.BooleanField(default=False)
    metodo_rebotado = models.CharField(max_length=200, null=True)
    parametros_rebotado = models.CharField(max_length=255, null=True)
    con_rechazado = models.BooleanField(default=False)
    metodo_rechazado = models.CharField(max_length=200, null=True)
    paramtros_rechazado = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.url)

    @classmethod
    def get_ws_conf(self):
        ws = WebServicesWebhooks.objects.all()[:1]
        if ws is not None:
            return ws
        else:
            return None
