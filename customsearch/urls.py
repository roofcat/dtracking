# -*- coding: utf-8 -*-


from django.conf.urls import include, url


from .views import IndexTemplateView
from .views import EmailSearchTemplateView
from .views import FolioSearchTemplateView
from .views import RutSearchTemplateView
from .views import FallidosSearchTemplateView
from .views import MontoSearchTemplateView
from .views import EmailDetailTemplateView
from .views import DynamicQueryTemplateView


urlpatterns = [
	# estas son las urls para las consultas que llenan la tabla html
    url(r'^$', IndexTemplateView.as_view(), name='index'),
    url(r'^email/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<correo>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', 
    	EmailSearchTemplateView.as_view()),
	url(r'^folio/(?P<folio>\d+)/$', FolioSearchTemplateView.as_view()),
	url(r'^rut/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<rut>\b\d{1,8}\-[K|0-9])/$', 
		RutSearchTemplateView.as_view()),
	url(r'^fallidos/(?P<date_from>\d+)/(?P<date_to>\d+)/$', 
		FallidosSearchTemplateView.as_view()),
	url(r'^montos/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<mount_from>\d+)/(?P<mount_to>\d+)/$', 
		MontoSearchTemplateView.as_view()),
	# consultas para el modal de detalle (cuando clickean un row de la tabla html)
	url(r'^email-detail/', EmailDetailTemplateView.as_view()),
	# consultas dinamicas
	url(r'^search/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<empresa>[\S]+)/(?P<correo>[\S]+)/(?P<folio>[\S]+)/(?P<rut>[\S]+)/(?P<mount_from>[\S]+)/(?P<mount_to>[\S]+)/(?P<fallidos>[\S]+)/', 
		DynamicQueryTemplateView.as_view()),
]
