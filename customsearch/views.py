# -*- coding: utf-8 -*-


from datetime import datetime
import json


from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


from autenticacion.views import LoginRequiredMixin
from emails.models import Email


timestamp_to_date = lambda x: datetime.fromtimestamp(x)


class EmailSearchTemplateView(LoginRequiredMixin, TemplateView):

	def get(self, request, date_from, date_to, correo, *args, **kwargs):
		try:
			if date_from and date_to and correo:
				display_start = request.GET['iDisplayStart']
				display_length = request.GET['iDisplayLength']
				echo = request.GET['sEcho']
				date_from = int(date_from, base=10)
				date_to = int(date_to, base=10)
				date_from = timestamp_to_date(date_from)
				date_to = timestamp_to_date(date_to)
				emails = Email.get_emails_by_dates(
					date_from, date_to, correo, 
					display_start=display_start, 
					display_length=display_length)
				data = {
					'sEcho': echo,
					'data': emails['data'],
					'iTotalDisplayRecords': emails['query_total'],
					'iTotalRecords': emails['query_total'],
				}
				data = json.dumps(data)
				return HttpResponse(data, content_type='application/json')
		except Exception, e:
			print e


class IndexTemplateView(LoginRequiredMixin, TemplateView):
	template_name = 'customsearch/index.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
