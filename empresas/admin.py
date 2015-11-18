# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import Empresa


class EmpresaAdmin(admin.ModelAdmin):
	list_filter = ('rut', 'empresa',)
	search_fields = ('rut', 'empresa',)


admin.site.register(Empresa, EmpresaAdmin)