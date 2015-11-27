# -*- coding: utf-8 -*-


from django.conf.urls import include, url


from .views import IndexTemplateView, EmailSearchTemplateView


urlpatterns = [
    url(r'^$', IndexTemplateView.as_view(), name='index'),
    url(r'^email/(?P<date_from>\d+)/(?P<date_to>\d+)/(?P<correo>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', 
    	EmailSearchTemplateView.as_view()),
    """
	url(r'^folio/$', ),
	url(r'^rut/$', ),
	url(r'^fallidos/$', ),
	url(r'^monto/$', ),
	"""
]
