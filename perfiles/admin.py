# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import Perfil


class PerfilAdmin(admin.ModelAdmin):
	list_display = ('usuario',)
	list_filter = ('empresas', 'usuario',)


admin.site.register(Perfil, PerfilAdmin)
