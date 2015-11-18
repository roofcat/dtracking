from django.contrib import admin


from .models import Email


class EmailAdmin(admin.ModelAdmin):
	list_filter = ('input_date', 'correo', 'rut_emisor', 'numero_folio', 'empresa',)
	search_fields = ('input_date', 'correo', 'rut_emisor', 'numero_folio', 'empresa',)


admin.site.register(Email, EmailAdmin)