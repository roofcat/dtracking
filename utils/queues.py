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

def delete_queue(email_id):
    if email_id is not None:
        context = {
            "email_id": email_id,
        }
        q = taskqueue.Queue("DeleteQueue")
        t = taskqueue.Task(url="/emails/queue/delete-email/", params=context)
        q.add(t)
        data = {"status": "ok"}
