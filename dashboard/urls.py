# -*- coding: utf-8 -*-


from django.conf.urls import include, url


from .views import IndexView, StatisticsView


urlpatterns = [
	url(r'^$', IndexView.as_view(), name="index"),
	url(r'^statistics/$', StatisticsView.as_view()),
]
