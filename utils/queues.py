# -*- coding: utf-8 -*-


from google.appengine.api import taskqueue


def input_queue(email_id):
    if email_id is not None:
        context = {
            "email_id": email_id,
        }
        q = taskqueue.Queue("InputQueue")
        t = taskqueue.Task(url="/emails/inputqueue/", params=context)
        q.add(t)


def report_queue(context):
    q = taskqueue.Queue("ReportQueue")
    t = taskqueue.Task(url="/reports/exportqueue/", params=context)
    q.add(t)
    data = {"status": "ok"}


def delete_file_queue(file_url):
    context = {
        "file_url": file_url,
    }
    q = taskqueue.Queue("DeleteFileQueue")
    t = taskqueue.Task(url="/emails/queue/delete-file/", params=context)
    q.add(t)
    data = {"status": "ok"}


def soap_ws_queue(context):
    q = taskqueue.Queue("SoapWSQueue")
    t = taskqueue.Task(url="/webservices/soap/", params=context)
    q.add(t)
    data = {"status": "ok"}


def rest_ws_queue(context):
    q = taskqueue.Queue("RestWSQueue")
    t = taskqueue.Task(url="/webservices/rest/", params=context)
    q.add(t)
    data = {"status": "ok"}
