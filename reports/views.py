# -*- coding: utf-8 -*-


from datetime import datetime
import json
import logging


from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


from .forms import ReportForm
from autenticacion.views import LoginRequiredMixin
from configuraciones.models import GeneralConfiguration
from emails.models import Email
from perfiles.models import Perfil
from utils.generics import timestamp_to_date
from utils.queues import report_queue
from utils.sendgrid_client import EmailClient
from utils.tablib_export import create_tablib


""" Serie de clases controladoras que reciben parametros
	para enviarlos en una cola controladora para enviar
	reporte por correo
"""


REPORT_FILE_FORMAT = 'xlsx'


def get_report_file_format():
	conf = GeneralConfiguration.get_configuration()
	if conf is not None:
		return conf.report_file_format
	else:
		return REPORT_FILE_FORMAT


class ReporteConsolidadoTemplateView(LoginRequiredMixin, TemplateView):
	""" Esta vista esta creada para extraer reportes consoliados
		dentro de algun periodo de tiempo en base a un rango de fechas
		desde - hasta
	"""

	def get(self, request, *args, **kwargs):
		perfil = Perfil.get_perfil(request.user)
		logging.info(perfil)
		data = {
			'es_admin': perfil.es_admin,
			'empresas': perfil.empresas.all(),
		}
		return render(request, 'reports/consolidados.html', data)

	def post(self, request, *args, **kwargs):
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
		empresa = request.POST['empresas']
		date_from = datetime.strptime(str(date_from), '%d/%m/%Y')
		date_to = datetime.strptime(str(date_to), '%d/%m/%Y')
		empresa = str(empresa)
		data = Email.get_emails_by_dates(date_from, date_to, empresa)
		report_file = create_tablib(data)

		if get_report_file_format() == 'xlsx':
			response = HttpResponse(report_file.xlsx, content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'attachment; filename="consolidado.xlsx"'
		elif get_report_file_format() == 'csv':
			response = HttpResponse(report_file.csv, content_type="text/csv")
			response['Content-Disposition'] = 'attachment; filename="consolidado.csv"'
		elif get_report_file_format() == 'tsv':
			response = HttpResponse(report_file.tsv, content_type="text/tsv")
			response['Content-Disposition'] = 'attachment; filename="consolidado.tsv"'
		else:
			response = HttpResponse(report_file.xlsx, content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'attachment; filename="consolidado.xlsx"'
		return response


class DynamicReportTemplateView(LoginRequiredMixin, TemplateView):

	def get(self, request, date_from, date_to, empresa, correo, folio, 
			rut, mount_from, mount_to, fallidos, *args, **kwargs):
		parameters = {}
		# preparación de parámetros
		date_from = int(date_from, base=10)
		date_to = int(date_to, base=10)
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

		context = dict()
		context['user_email'] = request.user.email
		context['file_name'] = 'reporte_dinamico.' + get_report_file_format()
		context['export_type'] = 'export_dynamic_emails'
		context['params'] = json.dumps(parameters)
		report_queue(context)
		data = {"status": "ok"}
		return HttpResponse(json.dumps(data), content_type='application/json')


class GeneralReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa, options, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'empresa': str(empresa),
                    'options': options,
                    'user_email': request.user.email,
                    'file_name': 'reporte_general.' + get_report_file_format(),
                    'export_type': 'export_general_email',
                }
                report_queue(context)
                data = {"status": "ok"}
                return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class SendedReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa, options, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'empresa': str(empresa),
                    'options': options,
                    'user_email': request.user.email,
                    'file_name': 'reporte_enviados.' + get_report_file_format(),
                    'export_type': 'export_sended_email',
                }
            report_queue(context)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class FailureReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa, options, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'empresa': str(empresa),
                    'options': options,
                    'user_email': request.user.email,
                    'file_name': 'reporte_fallidos.' + get_report_file_format(),
                    'export_type': 'export_failure_email',
                }
            report_queue(context)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class ByEmailReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, correo, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'email': str(correo).lower(),
                    'user_email': request.user.email,
                    'file_name': 'reporte_por_email.' + get_report_file_format(),
                    'export_type': 'export_search_by_email',
                }
            report_queue(context)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class ByFolioReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, folio, *args, **kwargs):
        try:
            if folio:
                context = {
                    'folio': int(folio, base=10),
                    'user_email': request.user.email,
                    'file_name': 'reporte_por_folio.' + get_report_file_format(),
                    'export_type': 'export_search_by_folio',
                }
                report_queue(context)
                data = {"status": "ok"}
                return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class ByRutReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, rut, *args, **kwargs):
        try:
            if date_from and date_to and rut:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'rut': str(rut).upper(),
                    'user_email': request.user.email,
                    'file_name': 'reporte_por_rut.' + get_report_file_format(),
                    'export_type': 'export_search_by_rut',
                }
            report_queue(context)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class ByMountReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, mount_from, mount_to, *args, **kwargs):
        try:
            if date_from and date_to and mount_from and mount_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'mount_from': mount_from,
                    'mount_to': mount_to,
                    'user_email': request.user.email,
                    'file_name': 'reporte_por_monto.' + get_report_file_format(),
                    'export_type': 'export_search_by_mount',
                }
            report_queue(context)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class QueueExportView(TemplateView):
	""" Controlador principal para generar 
	    los reportes y enviarlos por correo
	"""

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(QueueExportView, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logging.info(request.body)
		export_type = request.POST.get('export_type')
		if export_type == 'export_general_email':
			options = request.POST.get('options')
			empresa = request.POST.get('empresa')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			params = {}
			params['date_from'] = date_from
			params['date_to'] = date_to
			params['empresa'] = empresa
			params['options'] = options
			# Consulta
			data = Email.get_emails_by_dates_async(**params)
		elif export_type == 'export_sended_email':
			options = request.POST.get('options')
			empresa = request.POST.get('empresa')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			params = {}
			params['date_from'] = date_from
			params['date_to'] = date_to
			params['empresa'] = empresa
			params['options'] = options
			# Consulta
			data = Email.get_sended_emails_by_dates_async(**params)
		elif export_type == 'export_failure_email':
			options = request.POST.get('options')
			empresa = request.POST.get('empresa')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			params = {}
			params['date_from'] = date_from
			params['date_to'] = date_to
			params['empresa'] = empresa
			params['options'] = options
			# Consulta
			data = Email.get_failure_emails_by_dates_async(**params)
		elif export_type == 'export_search_by_email':
			correo = request.POST.get('email')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			# Consulta
			data = Email.get_emails_by_correo_async(
				date_from, date_to, correo)
		elif export_type == 'export_search_by_folio':
			folio = request.POST.get('folio')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			# Consulta
			data = Email.get_emails_by_folio_async(folio)
		elif export_type == 'export_search_by_rut':
			rut = request.POST.get('rut')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			# Consulta
			data = Email.get_emails_by_rut_receptor_async(
				date_from, date_to, rut)
		elif export_type == 'export_search_by_mount':
			mount_from = request.POST.get('mount_from')
			mount_to = request.POST.get('mount_to')
			mount_from = int(mount_from, base=10)
			mount_to = int(mount_to, base=10)
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			# Consulta
			data = Email.get_emails_by_mount_and_dates_async(
				date_from, date_to, mount_from, mount_to)
		elif export_type == 'export_dynamic_emails':
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			params = request.POST.get('params')
			params = json.loads(params)
			logging.info(params)
			data = Email.get_emails_by_dynamic_query_async(**params)
		# Creación del documento
		excel_report = create_tablib(data)
		# Crear objeto
		data = dict()
		data['name'] = file_name
		if get_report_file_format() == 'xlsx':
			data['report'] = excel_report.xlsx
		else:
			data['report'] = excel_report.csv
		# preparación de parametros
		mail = EmailClient()
		mail.send_report_to_user_with_attach(user_email, data)
		data = {"status": "ok"}
		return HttpResponse(json.dumps(data), content_type="application/json")
