# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from django.contrib import admin


from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from emails.views import EmailViewSet
from empresas.views import EmpresaViewSet


# sección de registro de apis rest con django-rest-framework
router = routers.DefaultRouter()
router.register(r'^emails', EmailViewSet)
router.register(r'^empresas', EmpresaViewSet)


urlpatterns = [
	# rutas de api rest
	url(r'^api/', include(router.urls)),
	# url(r'^api-auth/$', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api-token/', obtain_auth_token),
	
	# rutas de las paginas html del tracking
    url(r'^$', 'dashboard.views.index'),
    url(r'^customsearch/$', 'customsearch.views.index'),
    # url que recibe webhooks de sendgrid
    url(r'^webhook/$', 'webhooks.views.sendgrid_rest_webhook'),

    # rutas de autenticación de usuarios
    url(r'^login/', 'autenticacion.views.log_in'),
    url(r'^logout/', 'autenticacion.views.log_out'),

    # modulo Administrador Azurian
    url(r'^admin/', include(admin.site.urls)),
]
