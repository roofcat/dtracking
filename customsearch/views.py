# -*- coding: utf-8 -*-


import json
import logging


from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView


from autenticacion.views import LoginRequiredMixin
from emails.models import Email
from perfiles.models import Perfil
from tipodocumentos.models import TipoDocumento
from utils.generics import timestamp_to_date


class DynamicQueryTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa, correo, folio,
                rut, mount_from, mount_to, fallidos, *args, **kwargs):
        parameters = {}
        # preparación de parámetros
        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        date_from = timestamp_to_date(date_from)
        date_to = timestamp_to_date(date_to)
        parameters['date_from'] = date_from
        parameters['date_to'] = date_to
        if empresa == 'all':
            empresa = None
        parameters['empresa'] = empresa
        if correo == '-':
            correo = None
        parameters['correo'] = correo
        if folio == '-':
            folio = None
        parameters['folio'] = folio
        if rut == '-':
            rut = None
        parameters['rut'] = rut
        if mount_from == '-':
            mount_from = None
        else:
            mount_from = int(mount_from, base=10)
        parameters['mount_from'] = mount_from
        if mount_to == '-':
            mount_to = None
        else:
            mount_to = int(mount_to, base=10)
        parameters['mount_to'] = mount_to
        if fallidos == 'true':
            parameters['fallidos'] = True
        elif fallidos == 'false':
            parameters['fallidos'] = False
        else:
            parameters['fallidos'] = False
        # preparación de parámetros de paginación
        echo = request.GET['sEcho']
        display_start = request.GET['iDisplayStart']
        display_length = request.GET['iDisplayLength']
        parameters['display_start'] = int(display_start, base=10)
        parameters['display_length'] = int(display_length, base=10)
        emails = Email.get_emails_by_dynamic_query(**parameters)
        data = {
            'sEcho': echo,
            'data': emails['data'],
            'iTotalDisplayRecords': emails['query_total'],
            'iTotalRecords': emails['query_total'],
        }
        return HttpResponse(json.dumps(data), content_type='application/json')


class EmailDetailTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            pk = request.GET['pk']
            if pk:
                pk = int(pk, base=10)
                email = get_object_or_404(Email, pk=pk)
                email = model_to_dict(email)
                try:
                    # Intenta obtener el tipo de documento
                    tipo_dte = get_object_or_404(TipoDocumento, pk=email['tipo_dte'])
                    email['tipo_dte'] = str(email['tipo_dte']) + ' - ' + tipo_dte.nombre_documento
                except Exception, e:
                    logging.info(e)
                email['xml'] = email['xml'].name
                email['pdf'] = email['pdf'].name
                email['adjunto1'] = email['adjunto1'].name
                return HttpResponse(json.dumps(email), content_type='application/json')
        except Exception, e:
            logging.error(e)


class EmailSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, correo, *args, **kwargs):
        try:
            if date_from and date_to and correo:
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                display_start = int(display_start, base=10)
                display_length = int(display_length, base=10)
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
            logging.error(e)


class FolioSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, folio, *args, **kwargs):
        try:
            if folio:
                folio = int(folio, base=10)
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                display_start = int(display_start, base=10)
                display_length = int(display_length, base=10)
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
            logging.error(e)


class RutSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, rut, *args, **kwargs):
        try:
            if rut:
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                display_start = int(display_start, base=10)
                display_length = int(display_length, base=10)
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
            logging.error(e)


class FallidosSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, *args, **kwargs):
        try:
            if date_from and date_to:
                echo = request.GET['sEcho']
                display_start = request.GET['iDisplayStart']
                display_length = request.GET['iDisplayLength']
                display_start = int(display_start, base=10)
                display_length = int(display_length, base=10)
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
            logging.error(e)


class MontoSearchTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, mount_from, mount_to, *args, **kwargs):
        if date_from and date_to and mount_from and mount_to:
            echo = request.GET['sEcho']
            display_start = request.GET['iDisplayStart']
            display_length = request.GET['iDisplayLength']
            display_start = int(display_start, base=10)
            display_length = int(display_length, base=10)
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
        perfil = Perfil.get_perfil(request.user)
        logging.info(perfil.usuario)
        data = {
            'empresas': perfil.empresas.all(),
        }
        return render(request, self.template_name, data)
