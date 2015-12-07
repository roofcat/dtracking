# -*- coding: utf-8 -*-


from datetime import datetime
import calendar


from django.db import models


class Report(models.Model):
    input_date = models.DateField(auto_now_add=True, db_index=True)
    name = models.CharField(max_length=120)
    report = models.FileField(
        upload_to='reportes/%Y/%m/%d/{0}'.format(
        	calendar.timegm(datetime.utcnow().utctimetuple())))

    def __unicode__(self):
    	return self.name
