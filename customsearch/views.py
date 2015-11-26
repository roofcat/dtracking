# -*- coding: utf-8 -*-


from datetime import datetime
import json


from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


from autenticacion.views import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
	template_name = 'customsearch/index.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
