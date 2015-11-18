# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^$', 'emails.views.dashboard'),
    url(r'^customsearch/$', 'emails.views.customsearch'),

	# sistema de autenticación de usuarios
	url(r'^login/', 'autenticacion.views.log_in'),
	url(r'^logout/', 'autenticacion.views.log_out'),

    # modulo Administrador Azurian
    url(r'^admin/', include(admin.site.urls)),
]
