# -*- coding: utf-8 -*-


from datetime import datetime
import json


from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


from autenticacion.views import LoginRequiredMixin
from emails.models import Email
from perfiles.models import Perfil
from utils.generics import timestamp_to_date


class StatisticsView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
        empresa = request.GET['empresas']
        options = request.GET['options']
        try:
            # perfil = Perfil.get_perfil(request.user)
            if date_from and date_to:
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = timestamp_to_date(date_from)
                date_to = timestamp_to_date(date_to)
                statistic = Email.get_statistics_count_by_dates(date_from, date_to, empresa, options)
                results = Email.get_statistics_range_by_dates(date_from, date_to, empresa, options)
                data = {
                    'date_from': str(date_from),
                    'date_to': str(date_to),
                    'statistic': statistic,
                    'results': results,
                }
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')
        except Exception, e:
            print e


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        perfil = Perfil.get_perfil(request.user)
        print perfil
        data = {
            'es_admin': perfil.es_admin,
            'empresas': perfil.empresas.all(),
        }
        return render(request, self.template_name, data)
