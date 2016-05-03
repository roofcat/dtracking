# -*- coding: utf-8 -*-


from django.db import models


REPORT_FILE_FORMAT = (
    ('xlsx', 'xlsx'),
    ('csv', 'csv'),
)


class GeneralConfiguration(models.Model):
    report_row_max_length = models.IntegerField()
    report_file_format = models.CharField(max_length=100, choices=REPORT_FILE_FORMAT)

    @classmethod
    def get_configuration(self):
        try:
            return GeneralConfiguration.objects.all()[:1].get()
        except GeneralConfiguration.DoesNotExist:
            return None


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


class SoapWebService(models.Model):
    url = models.URLField(max_length=255)
    con_autenticacion = models.BooleanField(default=False, blank=True)
    usuario_autenticacion = models.CharField(max_length=200, null=True, blank=True)
    clave_autenticacion = models.CharField(max_length=200, null=True, blank=True)
    # documento
    con_objeto_documento = models.BooleanField(default=False)
    nombre_objeto_documento = models.CharField(max_length=200, null=True, blank=True)
    nombre_parametro_documento = models.CharField(max_length=200, null=True, blank=True)
    parametros_objeto_documento = models.CharField(max_length=255, null=True, blank=True)
    campos_objeto_documento = models.CharField(max_length=255, null=True, blank=True)
    # request
    con_objeto_request = models.BooleanField(default=False)
    nombre_objeto_request = models.CharField(max_length=200, null=True, blank=True)
    # default
    solo_default = models.BooleanField(default=False)
    metodo_default = models.CharField(max_length=200, null=True, blank=True)
    parametros_default = models.CharField(max_length=255, blank=True,
                                          help_text='Lista de parametros ordenados \
                                          por posición en el metodo del Web Service \
                                          separado por ; sin espacios ejemplo: \
										  "rut_emisor;numero_folio;input_date"')
    campos_default = models.CharField(max_length=255, null=True, blank=True)
    # procesados
    con_procesado = models.BooleanField(default=False, blank=True)
    metodo_procesado = models.CharField(max_length=200, null=True, blank=True)
    parametros_procesado = models.CharField(max_length=255, null=True, blank=True)
    campos_procesado = models.CharField(max_length=255, null=True, blank=True)
    # enviados
    con_enviado = models.BooleanField(default=False, blank=True)
    metodo_enviado = models.CharField(max_length=200, null=True, blank=True)
    parametros_enviado = models.CharField(max_length=255, null=True, blank=True)
    campos_enviado = models.CharField(max_length=255, null=True, blank=True)
    # leidos
    con_leido = models.BooleanField(default=False, blank=True)
    metodo_leido = models.CharField(max_length=200, null=True, blank=True)
    parametros_leido = models.CharField(max_length=255, null=True, blank=True)
    campos_leido = models.CharField(max_length=255, null=True, blank=True)
    # rebotados
    con_rebotado = models.BooleanField(default=False, blank=True)
    metodo_rebotado = models.CharField(max_length=200, null=True, blank=True)
    parametros_rebotado = models.CharField(max_length=255, null=True, blank=True)
    campos_rebotado = models.CharField(max_length=255, null=True, blank=True)
    # rechazados
    con_rechazado = models.BooleanField(default=False, blank=True)
    metodo_rechazado = models.CharField(max_length=200, null=True, blank=True)
    parametros_rechazado = models.CharField(max_length=200, null=True, blank=True)
    campos_rechazado = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.url)

    @classmethod
    def get_ws_conf(self):
        try:
            return SoapWebService.objects.all()[:1].get()
        except Exception, e:
            return None
