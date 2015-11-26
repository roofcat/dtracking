# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from django.contrib import admin


from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from emails.views import EmailViewSet
from empresas.views import EmpresaViewSet


# sección de registro de apis rest con django-rest-framework
router = routers.DefaultRouter()
# router.register(r'^emails', EmailViewSet)
# router.register(r'^empresas', EmpresaViewSet)


urlpatterns = [
    # rutas de api rest
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/$', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token/', obtain_auth_token),
    
    # rutas api rest heredadas de APIView
    url(r'^api/input/$', 'emails.views.email_dte_input_view'),
    url(r'^api/input/(?P<id>[0-9]+)/$', 'emails.views.email_dte_input_view'),

	# rutas de las paginas html del tracking
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^customsearch/', include('customsearch.urls', namespace='customsearch')),

    # url que recibe webhooks de sendgrid
    url(r'^webhook/$', 'webhooks.views.sendgrid_rest_webhook', name='webhook_rest'),

    # rutas de autenticación de usuarios
    url(r'^$', 'autenticacion.views.home_to_dashboard'),
    url(r'^login/', 'autenticacion.views.log_in', name='login'),
    url(r'^logout/', 'autenticacion.views.log_out', name='logout'),
    
    # modulo Administrador Azurian
    url(r'^admin/', include(admin.site.urls)),
]
