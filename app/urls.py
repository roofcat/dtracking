# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from django.contrib import admin


from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from autenticacion.views import log_in, log_out, home_to_dashboard
from emails.views import EmailDteInputView
from emails.views import queue_send_email
from emails.views import cron_send_delayed_email
from emails.views import cron_send_delayed_processed_email
from emails.views import cron_clean_emails_history
from emails.views import queue_delete_email
from empresas.views import EmpresaViewSet
from webhooks.views import sendgrid_rest_webhook, sendgrid_api_webhook


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
    url(r'^emails/inputqueue/', queue_send_email),

    # tarea cron que envia correos con pendiente
    url(r'^emails/cron/send-delayed/', cron_send_delayed_email),
    url(r'^emails/cron/send-delayed-processed/', cron_send_delayed_processed_email),
    url(r'^emails/cron/clean-history/', cron_clean_emails_history),

    # colas de tareas para correos
    url(r'^emails/queue/delete-email/', queue_delete_email),

	# rutas de las paginas html del tracking
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^customsearch/', include('customsearch.urls', namespace='customsearch')),

    # rutas para reportes
    url(r'^reports/', include('reports.urls', namespace='reports')),

    # url que recibe webhooks de sendgrid
    url(r'^webhook/', sendgrid_rest_webhook, name='webhook_rest'),
    url(r'^webhook-api/', sendgrid_api_webhook, name='webhook_rest'),

    # rutas de autenticación de usuarios
    url(r'^$', home_to_dashboard),
    url(r'^login/', log_in, name='login'),
    url(r'^logout/', log_out, name='logout'),
    
    # modulo Administrador Azurian
    url(r'^admin/', include(admin.site.urls)),
]
