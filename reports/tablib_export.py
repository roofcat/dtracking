# -*- coding: utf-8 -*-


from datetime import datetime
import logging
import pytz
import tablib


""" Esta función genera excel en tiempo real de ejecución 
    ya que recibe como parametro un arreglo de objetos
"""


timestamp_to_date = lambda x: datetime.fromtimestamp(x, tz=pytz.timezone("America/Santiago"))


def create_tablib(data):
    my_tab = tablib.Dataset()
    my_tab.headers = (
        'fecha', 'empresa', 'rut_receptor', 'rut_emisor', 'tipo_envio', 'tipo_dte',
        'numero_folio', 'resolucion_receptor', 'resolucion_emisor', 'monto', 'fecha_emision',
        'fecha_recepcion', 'estado_documento', 'tipo_operacion', 'tipo_receptor',
        'nombre_cliente', 'correo', 'asunto', 'fecha_procesado', 'procesado', 'fecha_envio',
        'enviado', 'respuesta_envio', 'fecha_primera_lectura', 'fecha_ultima_lectura',
        'abierto', 'ip_lector', 'navegador_lectura', 'cantidad_lectura', 'fecha_drop',
        'razon_drop', 'drop', 'fecha_rebote', 'rebote', 'motivo_rebote', 'estado_Rebote',
        'tipo_rebote', 'fecha_unsubscribe', 'unsubscribe_purchase', 'unsubscribe_id',
        'unsubscribe', 'click_ip', 'click_purchase', 'click_navegador', 'click_event',
        'click_email', 'fecha_click', 'click_url'
    )
    if data:
        for row in data:
            input_date = row.input_date
            if row.empresa:
                empresa = unicode(row.empresa)
            else:
                empresa = ''
            if row.rut_receptor:
                rut_receptor = unicode(row.rut_receptor)
            else:
                rut_receptor = ''
            if row.rut_emisor:
                rut_emisor = unicode(row.rut_emisor)
            else:
                rut_emisor = ''
            if row.tipo_envio:
                tipo_envio = unicode(row.tipo_envio)
            else:
                tipo_envio = ''
            if row.tipo_dte:
                tipo_dte = unicode(row.tipo_dte)
            else:
                tipo_dte = ''
            if row.numero_folio:
                numero_folio = row.numero_folio
            else:
                numero_folio = ''
            if row.resolucion_receptor:
                resolucion_receptor = row.resolucion_receptor
            else:
                resolucion_receptor = ''
            if row.resolucion_emisor:
                resolucion_emisor = row.resolucion_emisor
            else:
                resolucion_emisor = ''
            if row.monto:
                monto = row.monto
            else:
                monto = ''
            if row.fecha_emision:
                fecha_emision = row.fecha_emision
            else:
                fecha_emision = ''
            if row.fecha_recepcion:
                fecha_recepcion = row.fecha_recepcion
            else:
                fecha_recepcion = ''
            if row.estado_documento:
                estado_documento = row.estado_documento
            else:
                estado_documento = ''
            if row.tipo_operacion:
                tipo_operacion = unicode(row.tipo_operacion)
            else:
                tipo_operacion = ''
            if row.tipo_receptor:
                tipo_receptor = unicode(row.tipo_receptor)
            else:
                tipo_receptor = ''
            if row.nombre_cliente:
                nombre_cliente = unicode(row.nombre_cliente)
            else:
                nombre_cliente = ''
            if row.correo:
                correo = unicode(row.correo)
            else:
                correo = ''
            if row.asunto:
                asunto = unicode(row.asunto)
            else:
                asunto = ''
            if row.processed_date is not None:
                processed_date = timestamp_to_date(row.processed_date)
            else:
                processed_date = ''
            if row.processed_event:
                processed_event = unicode(row.processed_event).encode('utf-8')
            else:
                processed_event = ''
            if row.delivered_date is not None:
                delivered_date = timestamp_to_date(row.delivered_date)
            else:
                delivered_date = ''
            if row.delivered_event:
                delivered_event = unicode(row.delivered_event).encode('utf-8')
            else:
                delivered_event = ''
            if row.delivered_response:
                delivered_response = unicode(row.delivered_response).encode('utf-8')
            else:
                delivered_response = ''
            if row.opened_first_date is not None:
                opened_first_date = timestamp_to_date(row.opened_first_date)
            else:
                opened_first_date = ''
            if row.opened_last_date is not None:
                opened_last_date = timestamp_to_date(row.opened_last_date)
            else:
                opened_last_date = ''
            if row.opened_event:
                opened_event = unicode(row.opened_event).encode('utf-8')
            else:
                opened_event = ''
            if row.opened_ip:
                opened_ip = unicode(row.opened_ip).encode('utf-8')
            else:
                opened_ip = ''
            if row.opened_user_agent:
                opened_user_agent = unicode(row.opened_user_agent).encode('utf-8')
            else:
                opened_user_agent = ''
            if row.opened_count:
                opened_count = row.opened_count
            else:
                opened_count = ''
            if row.dropped_date is not None:
                dropped_date = timestamp_to_date(row.dropped_date)
            else:
                dropped_date = ''
            if row.dropped_reason:
                dropped_reason = unicode(row.dropped_reason).encode('utf-8')
            else:
                dropped_reason = ''
            if row.dropped_event:
                dropped_event = unicode(row.dropped_event).encode('utf-8')
            else:
                dropped_event = ''
            if row.bounce_date is not None:
                bounce_date = timestamp_to_date(row.bounce_date)
            else:
                bounce_date = ''
            if row.bounce_event:
                bounce_event = unicode(row.bounce_event).encode('utf-8')
            else:
                bounce_event = ''
            if row.bounce_reason:
                bounce_reason = unicode(row.bounce_reason).encode('utf-8')
            else:
                bounce_reason = ''
            if row.bounce_status:
                bounce_status = unicode(row.bounce_status).encode('utf-8')
            else:
                bounce_status = ''
            if row.bounce_type:
                bounce_type = unicode(row.bounce_type).encode('utf-8')
            else:
                bounce_type = ''
            if row.unsubscribe_date is not None:
                unsubscribe_date = timestamp_to_date(row.unsubscribe_date)
            else:
                unsubscribe_date = ''
            if row.unsubscribe_purchase:
                unsubscribe_purchase = unicode(row.unsubscribe_purchase).encode('utf-8')
            else:
                unsubscribe_purchase = ''
            if row.unsubscribe_id:
                unsubscribe_id = unicode(row.unsubscribe_id).encode('utf-8')
            else:
                unsubscribe_id = ''
            if row.unsubscribe_event:
                unsubscribe_event = unicode(row.unsubscribe_event).encode('utf-8')
            else:
                unsubscribe_event = ''
            if row.click_ip:
                click_ip = unicode(row.click_ip).encode('utf-8')
            else:
                click_ip = ''
            if row.click_purchase:
                click_purchase = unicode(row.click_purchase).encode('utf-8')
            else:
                click_purchase = ''
            if row.click_useragent:
                click_useragent = unicode(row.click_useragent).encode('utf-8')
            else:
                click_useragent = ''
            if row.click_event:
                click_event = unicode(row.click_event).encode('utf-8')
            else:
                click_event = ''
            if row.click_email:
                click_email = unicode(row.click_email).encode('utf-8')
            else:
                click_email = ''
            if row.click_date is not None:
                click_date = timestamp_to_date(row.click_date)
            else:
                click_date = ''
            if row.click_url:
                click_url = unicode(row.click_url).encode('utf-8')
            else:
                click_url = ''
            xlsx_row = (
                input_date, empresa, rut_receptor, rut_emisor, tipo_envio, tipo_dte,
                numero_folio, resolucion_receptor, resolucion_emisor, monto, 
                fecha_emision, fecha_recepcion, estado_documento, tipo_operacion, 
                tipo_receptor, nombre_cliente, correo, asunto, processed_date, 
                processed_event, delivered_date, delivered_event, delivered_response, 
                opened_first_date, opened_last_date, opened_event, opened_ip, 
                opened_user_agent, opened_count, dropped_date, dropped_reason, 
                dropped_event, bounce_date, bounce_event, bounce_reason, 
                bounce_status, bounce_type, unsubscribe_date, unsubscribe_purchase, 
                unsubscribe_id, unsubscribe_event, click_ip, click_purchase,
                click_useragent, click_event, click_email, click_date, click_url
            )
            my_tab.append(xlsx_row)
        return my_tab
