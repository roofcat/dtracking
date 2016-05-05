# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import EliminacionHistorico
from .models import GeneralConfiguration
from .models import SendgridConf
from .models import SoapWebService
from .models import TemplateReporte


class GeneralConfigurationAdmin(admin.ModelAdmin):
	list_display = ('report_row_max_length', 'report_file_format', 'report_file_zipped')


class SengridConfAdmin(admin.ModelAdmin):
	list_display = ('api_user', 'api_key',)


class TemplateReporteAdmin(admin.ModelAdmin):
	list_display = ('asunto_reporte', 'reporte_url',)


class EliminacionHistoricoAdmin(admin.ModelAdmin):
	list_display = ('activo', 'dias_a_eliminar',)


class SoapWebServiceAdmin(admin.ModelAdmin):
	list_display = ('url', 'con_autenticacion', 'solo_default',)


admin.site.register(SendgridConf, SengridConfAdmin)
admin.site.register(TemplateReporte, TemplateReporteAdmin)
admin.site.register(EliminacionHistorico, EliminacionHistoricoAdmin)
admin.site.register(SoapWebService, SoapWebServiceAdmin)
admin.site.register(GeneralConfiguration, GeneralConfigurationAdmin)
