# -*- coding: utf-8 -*-


from datetime import datetime
import json


from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


from autenticacion.views import LoginRequiredMixin
from emails.models import Email


class StatisticsView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
        options = request.GET['options']
        if date_from and date_to:
        	date_from = int(date_from, base=10)
        	date_to = int(date_to, base=10)
        	date_from = datetime.fromtimestamp(date_from)
        	date_to = datetime.fromtimestamp(date_to)
        	statistic = Email.get_statistics_count_by_dates(date_from, date_to)
        	data = {
        		'date_from': str(date_from),
        		'date_to': str(date_to),
        		'statistic': statistic,
        		'results': '',
        	}
    	print data
    	try:
        	data = json.dumps(data)
        	return HttpResponse(data, content_type='application/json')
    	except Exception, e:
    		print e


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
