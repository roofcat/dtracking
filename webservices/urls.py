# -*- coding: utf-8 -*-


from django.conf.urls import url

from .views import SendEmailEventToRestWsView
from .views import SendEmailEventToSoapWSView

urlpatterns = [
    url(r'^rest/$', SendEmailEventToRestWsView.as_view(), name='rest'),
    url(r'^soap/$', SendEmailEventToSoapWSView.as_view(), name='soap'),
]
