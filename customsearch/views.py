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
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = timestamp_to_date(date_from)
                date_to = timestamp_to_date(date_to)
                emails = Email.get_emails_by_correo(
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


class FolioSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, folio, *args, **kwargs):
        try:
            if folio:
                folio = int(folio, base=10)
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                emails = Email.get_emails_by_folio(folio,
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


class RutSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, rut, *args, **kwargs):
        try:
            if rut:
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = timestamp_to_date(date_from)
                date_to = timestamp_to_date(date_to)
                emails = Email.get_emails_by_rut_receptor(
                    date_from, date_to, rut,
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


class FallidosSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, *args, **kwargs):
        try:
            if date_from and date_to:
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = timestamp_to_date(date_from)
                date_to = timestamp_to_date(date_to)
                emails = Email.get_failure_emails_by_dates(
                    date_from, date_to,
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


class MontoSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, mount_from, mount_to, *args, **kwargs):
        if date_from and date_to and mount_from and mount_to:
            echo = request.GET['sEcho']
            display_start = request.GET['iDisplayStart']
            display_length = request.GET['iDisplayLength']
            date_from = int(date_from, base=10)
            date_to = int(date_to, base=10)
            date_from = timestamp_to_date(date_from)
            date_to = timestamp_to_date(date_to)
            mount_from = int(mount_from, base=10)
            mount_to = int(mount_to, base=10)
            emails = Email.get_emails_by_mount_and_dates(
                date_from, date_to, mount_from, mount_to,
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


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'customsearch/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
