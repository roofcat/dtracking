# -*- coding: utf-8 -*-


import json
import logging


from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from emails.models import Email


@csrf_exempt
@require_POST
def sendgrid_rest_webhook(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        logging.info(request_body)

        for body in request_body:
            try:
                evento_sendgrid = str(body['event']).decode('utf-8')
                email_id = str(body['email_id']).decode('utf-8')
                logging.info(evento_sendgrid)

                if evento_sendgrid and email_id:
                    email_id = int(email_id, base=10)
                    logging.info("es un webhook para el tracking")

                    if evento_sendgrid == 'processed':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(
                                body['smtp-id']).decode('utf-8')
                            email.processed_date = body['timestamp']
                            email.processed_event = evento_sendgrid
                            email.processed_sg_event_id = str(
                                body['sg_event_id']).decode('utf-8')
                            email.processed_sg_message_id = str(
                                body['sg_message_id']).decode('utf-8')
                            email.save()
                    elif evento_sendgrid == 'delivered':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(
                                body['smtp-id']).decode('utf-8')
                            email.delivered_date = body['timestamp']
                            email.delivered_event = evento_sendgrid
                            email.delivered_sg_event_id = str(
                                body['sg_event_id']).decode('utf-8')
                            email.delivered_sg_message_id = str(
                                body['sg_message_id']).decode('utf-8')
                            email.delivered_response = str(
                                body['response']).decode('utf-8')
                            email.save()
                    elif evento_sendgrid == 'open':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logging.info(email)
                            if email.opened_first_date is None:
                                email.opened_first_date = body['timestamp']
                            email.opened_last_date = body['timestamp']
                            email.opened_event = evento_sendgrid
                            email.opened_ip = str(body['ip']).decode('utf-8')
                            email.opened_user_agent = str(
                                body['useragent']).decode('utf-8')
                            email.opened_sg_event_id = str(
                                body['sg_event_id']).decode('utf-8')
                            email.opened_sg_message_id = str(
                                body['sg_message_id']).decode('utf-8')
                            email.opened_count += 1
                            email.save()
                    elif evento_sendgrid == 'dropped':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(
                                body['smtp-id']).decode('utf-8')
                            email.dropped_date = body['timestamp']
                            email.dropped_sg_event_id = str(
                                body['sg_event_id']).decode('utf-8')
                            email.dropped_sg_message_id = str(
                                body['sg_message_id']).decode('utf-8')
                            email.dropped_reason = str(
                                body['reason']).decode('utf-8')
                            email.dropped_event = evento_sendgrid
                            email.save()
                    elif evento_sendgrid == 'bounce':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(
                                body['smtp-id']).decode('utf-8')
                            email.bounce_date = body['timestamp']
                            email.bounce_event = evento_sendgrid
                            email.bounce_sg_event_id = str(
                                body['sg_event_id']).decode('utf-8')
                            email.bounce_sg_message_id = str(
                                body['sg_message_id']).decode('utf-8')
                            email.bounce_reason = str(
                                body['reason']).decode('utf-8')
                            email.bounce_status = str(
                                body['status']).decode('utf-8')
                            email.bounce_type = str(
                                body['type']).decode('utf-8')
                            email.save()
                    elif evento_sendgrid == 'unsubscribe':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logging.info(email)
                            email.unsubscribe_date = body['timestamp']
                            email.unsubscribe_uid = str(
                                body['uid']).decode('utf-8')
                            email.unsubscribe_purchase = str(
                                body['purchase']).decode('utf-8')
                            email.unsubscribe_id = str(
                                body['id']).decode('utf-8')
                            email.unsubscribe_event = evento_sendgrid
                            email.save()
                    elif evento_sendgrid == 'click':
                        email = Email.get_email_by_id(email_id)

                        if email is not None:
                            logging.info(email)
                            email.click_ip = str(body['ip']).decode('utf-8')
                            email.click_purchase = str(
                                body['purchase']).decode('utf-8')
                            email.click_useragent = str(
                                body['useragent']).decode('utf-8')
                            email.click_event = evento_sendgrid
                            email.click_email = str(
                                body['email']).decode('utf-8')
                            email.click_date = body['timestamp']
                            email.click_url = str(body['url']).decode('utf-8')
                            email.save()
                else:
                    logging.error(
                        "parametros incompletos, correo no corresponde.")
                return HttpResponse()
            except Exception, e:
                logging.error(e)
                return HttpResponse()


@csrf_exempt
@require_POST
def sendgrid_api_webhook(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        logging.info(request_body)

        for body in request_body:
            try:
                evento_sendgrid = str(body['event']).decode('utf-8')
                correo = str(body['email']).decode('utf-8')
                numero_folio = str(body['numero_folio']).decode('utf-8')
                tipo_dte = str(body['tipo_dte']).decode('utf-8')
                logging.info(evento_sendgrid)

                if evento_sendgrid and correo and numero_folio and tipo_dte is not None:
                    email_id = int(email_id, base=10)
                    logging.info("es un webhook para el tracking")

                    if evento_sendgrid == 'processed':
                        email = Email.get_email(correo, numero_folio, tipo_dte)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.processed_date = body['timestamp']
                            email.processed_event = evento_sendgrid
                            email.processed_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.processed_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.save()
                        else:
							email = Email.set_default_fields(body)
							# parametros del evento
							email.smtp_id = str(
							body['smtp-id']).decode('utf-8')
							email.processed_date = body['timestamp']
							email.processed_event = evento_sendgrid
							email.processed_sg_event_id = str(body['sg_event_id']).decode('utf-8')
							email.processed_sg_message_id = str(body['sg_message_id']).decode('utf-8')
							email.save()
                    elif evento_sendgrid == 'delivered':
                        email = Email.get_email(correo, numero_folio, tipo_dte)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.delivered_date = body['timestamp']
                            email.delivered_event = evento_sendgrid
                            email.delivered_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.delivered_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.delivered_response = str(body['response']).decode('utf-8')
                            email.save()
                        else:
							email = Email.set_default_fields(body)
							# parametros del evento
							email.smtp_id = str(body['smtp-id']).decode('utf-8')
							email.delivered_date = body['timestamp']
							email.delivered_event = evento_sendgrid
							email.delivered_sg_event_id = str(body['sg_event_id']).decode('utf-8')
							email.delivered_sg_message_id = str(body['sg_message_id']).decode('utf-8')
							email.delivered_response = str(body['response']).decode('utf-8')
							email.save()
                    elif evento_sendgrid == 'open':
                        email = Email.get_email(correo, numero_folio, tipo_dte)

                        if email is not None:
                            logging.info(email)
                            if email.opened_first_date is None:
                                email.opened_first_date = body['timestamp']
                            email.opened_last_date = body['timestamp']
                            email.opened_event = evento_sendgrid
                            email.opened_ip = str(body['ip']).decode('utf-8')
                            email.opened_user_agent = str(body['useragent']).decode('utf-8')
                            email.opened_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.opened_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.opened_count += 1
                            email.save()
                        else:
							email = Email.set_default_fields(body)
							# parametros del evento
							if email.opened_first_date is None:
								email.opened_first_date = body['timestamp']
							email.opened_last_date = body['timestamp']
							email.opened_event = evento_sendgrid
							email.opened_ip = str(body['ip']).decode('utf-8')
							email.opened_user_agent = str(body['useragent']).decode('utf-8')
							email.opened_sg_event_id = str(body['sg_event_id']).decode('utf-8')
							email.opened_sg_message_id = str(body['sg_message_id']).decode('utf-8')
							email.opened_count += 1
							email.save()
                    elif evento_sendgrid == 'dropped':
                        email = Email.get_email(correo, numero_folio, tipo_dte)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.dropped_date = body['timestamp']
                            email.dropped_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.dropped_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.dropped_reason = str(body['reason']).decode('utf-8')
                            email.dropped_event = evento_sendgrid
                            email.save()
                        else:
							email = Email.set_default_fields(body)
							# parametros del evento
							email.smtp_id = str(body['smtp-id']).decode('utf-8')
							email.dropped_date = body['timestamp']
							email.dropped_sg_event_id = str(body['sg_event_id']).decode('utf-8')
							email.dropped_sg_message_id = str(body['sg_message_id']).decode('utf-8')
							email.dropped_reason = str(body['reason']).decode('utf-8')
							email.dropped_event = evento_sendgrid
							email.save()
                    elif evento_sendgrid == 'bounce':
                        email = Email.get_email(correo, numero_folio, tipo_dte)

                        if email is not None:
                            logging.info(email)
                            email.smtp_id = str(body['smtp-id']).decode('utf-8')
                            email.bounce_date = body['timestamp']
                            email.bounce_event = evento_sendgrid
                            email.bounce_sg_event_id = str(body['sg_event_id']).decode('utf-8')
                            email.bounce_sg_message_id = str(body['sg_message_id']).decode('utf-8')
                            email.bounce_reason = str(body['reason']).decode('utf-8')
                            email.bounce_status = str(body['status']).decode('utf-8')
                            email.bounce_type = str(body['type']).decode('utf-8')
                            email.save()
                        else:
							email = Email.set_default_fields(body)
							# parametros del evento
							email.smtp_id = str(body['smtp-id']).decode('utf-8')
							email.bounce_date = body['timestamp']
							email.bounce_event = evento_sendgrid
							email.bounce_sg_event_id = str(body['sg_event_id']).decode('utf-8')
							email.bounce_sg_message_id = str(body['sg_message_id']).decode('utf-8')
							email.bounce_reason = str(body['reason']).decode('utf-8')
							email.bounce_status = str(body['status']).decode('utf-8')
							email.bounce_type = str(body['type']).decode('utf-8')
							email.save()
                    elif evento_sendgrid == 'unsubscribe':
                        email = Email.get_email(correo, numero_folio, tipo_dte)

                        if email is not None:
                            logging.info(email)
                            email.unsubscribe_date = body['timestamp']
                            email.unsubscribe_uid = str(body['uid']).decode('utf-8')
                            email.unsubscribe_purchase = str(body['purchase']).decode('utf-8')
                            email.unsubscribe_id = str(body['id']).decode('utf-8')
                            email.unsubscribe_event = evento_sendgrid
                            email.save()
                        else:
							email = Email.set_default_fields(body)
							# parametros del evento
							email.unsubscribe_date = body['timestamp']
							email.unsubscribe_uid = str(body['uid']).decode('utf-8')
							email.unsubscribe_purchase = str(body['purchase']).decode('utf-8')
							email.unsubscribe_id = str(body['id']).decode('utf-8')
							email.unsubscribe_event = evento_sendgrid
							email.save()
                    elif evento_sendgrid == 'click':
                        email = Email.get_email(correo, numero_folio, tipo_dte)

                        if email is not None:
                            logging.info(email)
                            email.click_ip = str(body['ip']).decode('utf-8')
                            email.click_purchase = str(body['purchase']).decode('utf-8')
                            email.click_useragent = str(body['useragent']).decode('utf-8')
                            email.click_event = evento_sendgrid
                            email.click_email = str(body['email']).decode('utf-8')
                            email.click_date = body['timestamp']
                            email.click_url = str(body['url']).decode('utf-8')
                            email.save()
                        else:
							email = Email.set_default_fields(body)
							# parametros del evento
							email.click_ip = str(body['ip']).decode('utf-8')
							email.click_purchase = str(body['purchase']).decode('utf-8')
							email.click_useragent = str(body['useragent']).decode('utf-8')
							email.click_event = evento_sendgrid
							email.click_email = str(body['email']).decode('utf-8')
							email.click_date = body['timestamp']
							email.click_url = str(body['url']).decode('utf-8')
							email.save()
                else:
                    logging.error(
                        "parametros incompletos, correo no corresponde.")
                return HttpResponse()
            except Exception, e:
                logging.error(e)
                return HttpResponse()
