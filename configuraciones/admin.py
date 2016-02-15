# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import SendgridConf
from .models import TemplateReporte
from .models import EliminacionHistorico
from .models import WebServicesWebhook


class SengridConfAdmin(admin.ModelAdmin):
	list_display = ('api_user', 'api_key',)


class TemplateReporteAdmin(admin.ModelAdmin):
	list_display = ('asunto_reporte', 'reporte_url',)


class EliminacionHistoricoAdmin(admin.ModelAdmin):
	list_display = ('activo', 'dias_a_eliminar',)


class WebServicesWebhookAdmin(admin.ModelAdmin):
	list_display = ('url', 'con_autenticacion', 'solo_default',)


admin.site.register(SendgridConf, SengridConfAdmin)
admin.site.register(TemplateReporte, TemplateReporteAdmin)
admin.site.register(EliminacionHistorico, EliminacionHistoricoAdmin)
admin.site.register(WebServicesWebhook, WebServicesWebhookAdmin)
