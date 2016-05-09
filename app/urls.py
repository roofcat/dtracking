# -*- coding: utf-8 -*-


from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve


from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from autenticacion.views import log_in, log_out, home_to_dashboard, ProfileTemplateView
from emails.views import EmailDteInputView
from emails.views import QueueSendEmailView
from emails.views import CronSendDelayedEmailView
from emails.views import CronSendDelayedProcessedEmailView
from emails.views import CronCleanEmailsHistoryView
from emails.views import DeleteEmailFileView
from empresas.views import EmpresaViewSet
from webhooks.views import SendGridRestWebhookView, SendGridApiWebhookView


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
    # en esta ruta entran las peticiones de correo desde un DTE
    url(r'^api/input/', EmailDteInputView.as_view()),
    
    # luego el tracking lo pasa a esta cola para 
    # luego enviar el correo por sendgrid
    url(r'^emails/inputqueue/', QueueSendEmailView.as_view()),

    # tarea cron que envia correos con pendiente
    url(r'^emails/cron/send-delayed/', CronSendDelayedEmailView.as_view()),
    url(r'^emails/cron/send-delayed-processed/', CronSendDelayedProcessedEmailView.as_view()),
    url(r'^emails/cron/clean-history/', CronCleanEmailsHistoryView.as_view()),

    # colas de tareas
    url(r'^emails/queue/delete-file/', DeleteEmailFileView.as_view()),

	# rutas de las paginas html del tracking
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^customsearch/', include('customsearch.urls', namespace='customsearch')),
    url(r'^webhook-api/', SendGridApiWebhookView.as_view(), name='webhook_api'),

    # rutas para reportes
    url(r'^reports/', include('reports.urls', namespace='reports')),

    # url que recibe webhooks de sendgrid
    url(r'^webhook/', SendGridRestWebhookView.as_view(), name='webhook_rest'),
    url(r'^resumen/',include('resumen.urls', namespace="resumen")),

    # url de manejo de reenvio de eventos a WS de clientes
    url(r'^webservices/', include('webservices.urls', namespace='webservices')),

    # rutas de autenticación de usuarios
    url(r'^$', home_to_dashboard),
    url(r'^login/', log_in, name='login'),
    url(r'^logout/', log_out, name='logout'),
    url(r'^profile/', ProfileTemplateView.as_view(), name='profile'),
    
    # modulo Administrador Azurian
    url(r'^admin/', include(admin.site.urls)),

    # rutas estaticas
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
