# -*- coding: utf-8 -*-


from datetime import datetime
import json


from google.appengine.api import taskqueue


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView


from .forms import ReportForm
from .tablib_export import create_tablib
from autenticacion.views import LoginRequiredMixin
from emails.models import Email
from sendgrid_manager.sendgrid_client import EmailClient


# Función lambda para convertir una fecha unix a datetime
timestamp_to_date = lambda x: datetime.fromtimestamp(x)


""" Serie de clases controladoras que reciben parametros
	para enviarlos en una cola controladora para enviar
	reporte por correo
"""


class GeneralReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, options, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'options': options,
                    'user_email': request.user.email,
                    'file_name': 'reporte_general.xlsx',
                    'export_type': 'export_general_email',
                }
                q = taskqueue.Queue("ReportQueue")
                t = taskqueue.Task(url="/reports/exportqueue/", params=context)
                q.add(t)
                data = {"status": "ok"}
                return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print e


class SendedReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, options, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'options': options,
                    'user_email': request.user.email,
                    'file_name': 'reporte_enviados.xlsx',
                    'export_type': 'export_sended_email',
                }
            q = taskqueue.Queue("ReportQueue")
            t = taskqueue.Task(url="/reports/exportqueue/", params=context)
            q.add(t)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print e


class FailureReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, options, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'options': options,
                    'user_email': request.user.email,
                    'file_name': 'reporte_fallidos.xlsx',
                    'export_type': 'export_failure_email',
                }
            q = taskqueue.Queue("ReportQueue")
            t = taskqueue.Task(url="/reports/exportqueue/", params=context)
            q.add(t)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print e


class ByEmailReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, email, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'email': str(email).lower(),
                    'user_email': request.user.email,
                    'file_name': 'reporte_por_email.xlsx',
                    'export_type': 'export_search_by_email',
                }
            q = taskqueue.Queue("ReportQueue")
            t = taskqueue.Task(url="/reports/exportqueue/", params=context)
            q.add(t)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print e


class ByFolioReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, folio, *args, **kwargs):
        try:
            if folio:
                context = {
                    'folio': int(folio, base=10),
                    'user_email': request.user.email,
                    'file_name': 'reporte_por_folio.xlsx',
                    'export_type': 'export_search_by_folio',
                }
                q = taskqueue.Queue("ReportQueue")
                t = taskqueue.Task(url="/reports/exportqueue/", params=context)
                q.add(t)
                data = {"status": "ok"}
                return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print e


class ByRutReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'rut': str(rut).upper(),
                    'user_email': request.user.email,
                    'file_name': 'reporte_por_rut.xlsx',
                    'export_type': 'export_search_by_rut',
                }
            q = taskqueue.Queue("ReportQueue")
            t = taskqueue.Task(url="/reports/exportqueue/", params=context)
            q.add(t)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print e


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
                    'file_name': 'reporte_por_monto.xlsx',
                    'export_type': 'export_search_by_mount',
                }
            q = taskqueue.Queue("ReportQueue")
            t = taskqueue.Task(url="/reports/exportqueue/", params=context)
            q.add(t)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            print e


@csrf_exempt
@require_POST
def queue_export(request):
	""" Controlador principal para generar 
	    los reportes y enviarlos por correo
	"""
	if request.method == 'POST':
		print request.body
		export_type = request.POST.get('export_type')
		if export_type == 'export_general_email':
			options = request.POST.get('options')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			# Consulta
			data = Email.get_emails_by_dates_async(
				date_from, date_to, options)
		elif export_type == 'export_sended_email':
			options = request.POST.get('options')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			# Consulta
			data = Email.get_sended_emails_by_dates_async(
				date_from, date_to, options)
		elif export_type == 'export_failure_email':
			options = request.POST.get('options')
			user_email = request.POST.get('user_email')
			file_name = request.POST.get('file_name')
			date_from = request.POST.get('date_from')
			date_to = request.POST.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = timestamp_to_date(date_from)
			date_to = timestamp_to_date(date_to)
			# Consulta
			data = Email.get_failure_emails_by_dates_async(
				date_from, date_to, options)
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
		# Creación del documento
		excel_report = create_tablib(data)
		#new_excel = open(excel_report.xlsx, "rb")
		# Crear objeto
		data = {
			'name': file_name,
			'report': excel_report.xlsx,
		}
		report = ReportForm(data)
		print "imprimir ReportForm"
		report.name = file_name
		report.report = excel_report.xlsx
		print report.is_valid()
		print report.errors
		print "se guardo el reporte"
		# preparación de parametros
		mail = EmailClient()
		mail.send_report_to_user_with_attach(user_email, data)
		data = {"status": "ok"}
		return HttpResponse(json.dumps(data), content_type="application/json")
