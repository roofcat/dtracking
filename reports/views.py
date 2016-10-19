# -*- coding: utf-8 -*-


from datetime import datetime
import json
import logging
from StringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from autenticacion.views import LoginRequiredMixin
from configuraciones.models import GeneralConfiguration
from emails.models import Email
from perfiles.models import Perfil
from utils.generics import timestamp_to_date
from utils.generics import get_date_to_string
from utils.queues import report_queue
from utils.sendgrid_client import EmailClient
from utils.tablib_export import create_tablib

REPORT_FILE_FORMAT = 'xlsx'


def get_report_file_format(empresa_id):
    conf = GeneralConfiguration.get_configuration(empresa_id)
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
        report_file = create_tablib(data, empresa)

        report_file_format = get_report_file_format(empresa)

        if report_file_format == 'xlsx':
            response_file = report_file.xlsx
            response_filename = 'consolidado' + get_date_to_string() + report_file_format
            response_filetype = 'application/vnd.ms-excel'
        elif report_file_format == 'tsv':
            response_file = report_file.tsv
            response_filename = 'consolidado' + get_date_to_string() + report_file_format
            response_filetype = 'text/tsv'
        else:
            response_file = report_file.csv
            response_filename = 'consolidado' + get_date_to_string() + report_file_format
            response_filetype = 'text/csv'

        general_conf = GeneralConfiguration.get_configuration(empresa)

        if general_conf is not None and general_conf.report_file_zipped:
            # ejecutar proceso de comprimir reporte
            in_memory = StringIO()

            with ZipFile(in_memory, 'w') as archive:
                archive.writestr(response_filename, str(response_file), ZIP_DEFLATED)

            response = HttpResponse(in_memory.getvalue(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'attachment; filename="reporte.zip"'
            return response
        else:
            # retornar el reporte
            response = HttpResponse(response_file, content_type=response_filetype)
            response['Content-Disposition'] = 'attachment; filename="' + response_filename + '"'
            return response


class DynamicReportTemplateView(LoginRequiredMixin, TemplateView):
    def get(self, request, date_from, date_to, empresa, correo, folio,
            rut, mount_from, mount_to, fallidos, op1, op2, op3, *args, **kwargs):
        parameters = dict()
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
        if op1 == '-':
            parameters['opcional1'] = None
        else:
            parameters['opcional1'] = op1
        if op2 == '-':
            parameters['opcional2'] = None
        else:
            parameters['opcional2'] = op2
        if op3 == '-':
            parameters['opcional3'] = None
        else:
            parameters['opcional3'] = op3

        report_file_format = get_report_file_format(empresa)

        context = dict()
        context['user_email'] = request.user.email
        context['file_name'] = 'reporte_dinamico' + get_date_to_string() + report_file_format
        context['export_type'] = 'export_dynamic_emails'
        context['empresa'] = empresa
        context['params'] = json.dumps(parameters)
        report_queue(context)
        data = {"status": "ok"}
        return HttpResponse(json.dumps(data), content_type='application/json')


class GeneralReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa, tipo_receptor, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'empresa': str(empresa),
                    'tipo_receptor': tipo_receptor,
                    'user_email': request.user.email,
                    'file_name': 'reporte_general' + get_date_to_string() + get_report_file_format(empresa),
                    'export_type': 'export_general_email',
                }
                report_queue(context)
                data = {"status": "ok"}
                return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class SendedReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa, tipo_receptor, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'empresa': str(empresa),
                    'tipo_receptor': tipo_receptor,
                    'user_email': request.user.email,
                    'file_name': 'reporte_enviados' + get_date_to_string() + get_report_file_format(empresa),
                    'export_type': 'export_sended_email',
                }
            report_queue(context)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception, e:
            logging.error(e)


class FailureReportTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, date_from, date_to, empresa, tipo_receptor, *args, **kwargs):
        try:
            if date_from and date_to:
                context = {
                    'date_from': int(date_from, base=10),
                    'date_to': int(date_to, base=10),
                    'empresa': str(empresa),
                    'tipo_receptor': str(tipo_receptor),
                    'user_email': request.user.email,
                    'file_name': 'reporte_fallidos' + get_date_to_string() + get_report_file_format(empresa),
                    'export_type': 'export_failure_email',
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
            tipo_receptor = request.POST.get('tipo_receptor')
            empresa = request.POST.get('empresa')
            user_email = request.POST.get('user_email')
            file_name = request.POST.get('file_name')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            date_from = int(date_from, base=10)
            date_to = int(date_to, base=10)
            date_from = timestamp_to_date(date_from)
            date_to = timestamp_to_date(date_to)
            params = dict()
            params['date_from'] = date_from
            params['date_to'] = date_to
            params['empresa'] = empresa
            params['tipo_receptor'] = tipo_receptor
            # Consulta
            data = Email.get_emails_by_dates_async(**params)
        elif export_type == 'export_sended_email':
            tipo_receptor = request.POST.get('tipo_receptor')
            empresa = request.POST.get('empresa')
            user_email = request.POST.get('user_email')
            file_name = request.POST.get('file_name')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            date_from = int(date_from, base=10)
            date_to = int(date_to, base=10)
            date_from = timestamp_to_date(date_from)
            date_to = timestamp_to_date(date_to)
            params = dict()
            params['date_from'] = date_from
            params['date_to'] = date_to
            params['empresa'] = empresa
            params['tipo_receptor'] = tipo_receptor
            # Consulta
            data = Email.get_sended_emails_by_dates_async(**params)
        elif export_type == 'export_failure_email':
            tipo_receptor = request.POST.get('tipo_receptor')
            empresa = request.POST.get('empresa')
            user_email = request.POST.get('user_email')
            file_name = request.POST.get('file_name')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            date_from = int(date_from, base=10)
            date_to = int(date_to, base=10)
            date_from = timestamp_to_date(date_from)
            date_to = timestamp_to_date(date_to)
            params = dict()
            params['date_from'] = date_from
            params['date_to'] = date_to
            params['empresa'] = empresa
            params['tipo_receptor'] = tipo_receptor
            # Consulta
            data = Email.get_failure_emails_by_dates_async(**params)
        elif export_type == 'export_dynamic_emails':
            user_email = request.POST.get('user_email')
            empresa = request.POST.get('empresa')
            file_name = request.POST.get('file_name')
            params = request.POST.get('params')
            params = json.loads(params)
            logging.info(params)
            data = Email.get_emails_by_dynamic_query_async(**params)

        if data is not None:
            # Creación del documento
            report_file = create_tablib(data, empresa)

            # evaluacion del formato del archivo reporte
            report_file_format = get_report_file_format(empresa)
            if report_file_format == 'xlsx':
                response_file = report_file.xlsx
                response_filename = file_name
            elif report_file_format == 'tsv':
                response_file = report_file.tsv
                response_filename = file_name
            else:
                response_file = report_file.csv
                response_filename = file_name

            # evaluar si el archivo es comprimido en zip
            general_conf = GeneralConfiguration.get_configuration(empresa)

            if general_conf is not None and general_conf.report_file_zipped:
                # ejecutar proceso de comprimir reporte
                in_memory = StringIO()

                with ZipFile(in_memory, 'w') as archive:
                    archive.writestr(response_filename, str(response_file), ZIP_DEFLATED)

                response_file = in_memory.getvalue()
                response_filename = file_name + '.zip'

            # Crear objeto para enviarlo por correo
            data = dict()
            data['name'] = response_filename
            data['report'] = response_file

            # preparación de parametros
            mail = EmailClient(empresa)
            mail.send_report_to_user_with_attach(user_email, data)
            data = {"status": "ok"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            logging.info("No se crear el archivo reporte por consulta vacía.")
            data = {"status": "consulta vacía"}
            return HttpResponse(json.dumps(data), content_type="application/json")
