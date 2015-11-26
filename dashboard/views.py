# -*- coding: utf-8 -*-


from datetime import datetime
import json


from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
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
        	count_total = Email.objects.filter(
        		input_date__range=(date_from, date_to)).count()
        	count_processed = Email.objects.filter(
        		input_date__range=(date_from, date_to),
        		processed_event='processed').count()
        	count_delivered = Email.objects.filter(
        		input_date__range=(date_from, date_to), 
        		delivered_event='delivered').count()
        	count_opened = Email.objects.filter(
        		input_date__range=(date_from, date_to), 
        		opened_event='open').count()
        	count_dropped = Email.objects.filter(
        		input_date__range=(date_from, date_to), 
        		dropped_event='dropped').count()
        	count_bounce = Email.objects.filter(
        		input_date__range=(date_from, date_to), 
        		bounce_event='bounce').count()
        	statistic = {
        		'total': count_total,
        		'processed': count_processed,
        		'delivered': count_delivered,
        		'opened': count_opened,
        		'dropped': count_dropped,
        		'bounced': count_bounce,
        	}
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
