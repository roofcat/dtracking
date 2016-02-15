# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import SendgridConf
from .models import TemplateReporte
from .models import EliminacionHistorico
from .models import WebServicesWebhooks


class SengridConfAdmin(admin.ModelAdmin):
	list_display = ('api_user', 'api_key',)


class TemplateReporteAdmin(admin.ModelAdmin):
	list_display = ('asunto_reporte', 'reporte_url',)


class EliminacionHistoricoAdmin(admin.ModelAdmin):
	list_display = ('activo', 'dias_a_eliminar',)


class WebServicesWebhooksAdmin(admin.ModelAdmin):
	list_display = ('url', 'parametros',)


admin.site.register(SendgridConf, SengridConfAdmin)
admin.site.register(TemplateReporte, TemplateReporteAdmin)
admin.site.register(EliminacionHistorico, EliminacionHistoricoAdmin)
admin.site.register(WebServicesWebhooks, WebServicesWebhooksAdmin)
