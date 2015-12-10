# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from django.contrib import admin


from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from autenticacion.views import log_in, log_out, home_to_dashboard
from emails.views import EmailDteInputView, queue_send_email
from empresas.views import EmpresaViewSet
from webhooks.views import sendgrid_rest_webhook


# sección de registro de apis rest con django-rest-framework
router = routers.DefaultRouter()
# router.register(r'^emails', EmailViewSet)
# router.register(r'^empresas', EmpresaViewSet)


urlpatterns = [
    # rutas de api rest
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token/', obtain_auth_token),
    
    # rutas api rest heredadas de APIView
    url(r'^api/input/', EmailDteInputView.as_view()),
    url(r'^api/input/inputqueue/', queue_send_email),

	# rutas de las paginas html del tracking
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^customsearch/', include('customsearch.urls', namespace='customsearch')),

    # rutas para reportes
    url(r'^reports/', include('reports.urls', namespace='reports')),

    # url que recibe webhooks de sendgrid
    url(r'^webhook/', sendgrid_rest_webhook, name='webhook_rest'),

    # rutas de autenticación de usuarios
    url(r'^$', home_to_dashboard),
    url(r'^login/', log_in, name='login'),
    url(r'^logout/', log_out, name='logout'),
    
    # modulo Administrador Azurian
    url(r'^admin/', include(admin.site.urls)),
]
