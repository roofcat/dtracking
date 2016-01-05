# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import Perfil


class PerfilAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'es_admin',)
	list_filter = ('es_admin', 'empresa', 'usuario',)


admin.site.register(Perfil, PerfilAdmin)