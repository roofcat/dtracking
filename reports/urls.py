# -*- coding: utf-8 -*-


from django.conf.urls import include, url


from .views import GeneralReportTemplateView
from .views import SendedReportTemplateView 
from .views import FailureReportTemplateView
from .views import ByEmailReportTemplateView
from .views import ByFolioReportTemplateView
from .views import ByRutReportTemplateView
from .views import ByMountReportTemplateView
from .views import queue_export

urlpatterns = [
	# urls para generar reportes
	url(r'^general/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<options>[\w.%+-]+)/$', 
		GeneralReportTemplateView.as_view()),
	url(r'^sended/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<options>[\w.%+-]+)/$', 
		SendedReportTemplateView.as_view()),
	url(r'^failure/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<options>[\w.%+-]+)/$', 
		FailureReportTemplateView.as_view()),
	url(r'^email/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<correo>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', 
		ByEmailReportTemplateView.as_view()),
	url(r'^folio/(?P<folio>\d+)/$', ByFolioReportTemplateView.as_view()),
	url(r'^rut/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<rut>\b\d{1,8}\-[K|0-9])/$', 
		ByRutReportTemplateView.as_view()),
	url(r'^mount/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<mount_from>\d+)/(?P<mount_to>\d+)/$', 
		ByMountReportTemplateView.as_view()),

	# ruta de cola de tarea TaskQueue
	url(r'^exportqueue/$', queue_export),
]