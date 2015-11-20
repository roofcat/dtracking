# -*- coding: utf-8 -*-


import datetime
import json
import logging


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from emails.models import Email


@csrf_exempt
@require_POST
def sendgrid_rest_webhook(request):
	if request.method == 'POST':
		request_body = json.loads(request.body)
		logging.info(request_body)
		for body in request_body:
			logging.info(body)
			evento_sendgrid = str(body['event'])
			correo = str(body['email'])
			numero_folio = str(body['numero_folio'])
			tipo_dte = str(body['tipo_dte'])
			logging.info(evento_sendgrid)

			if evento_sendgrid == 'processed':
				pass
			elif evento_sendgrid == 'delivered':
				pass
			elif evento_sendgrid == 'open':
				pass
			elif evento_sendgrid == 'dropped':
				pass
			elif evento_sendgrid == 'bounce':
				pass
			elif evento_sendgrid == 'unsubscribe':
				pass
			elif evento_sendgrid == 'click':
				pass
		return HttpResponse()
