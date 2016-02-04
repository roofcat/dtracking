# -*- coding: utf-8 -*-


from datetime import datetime
import pytz


timestamp_to_date = lambda x: datetime.fromtimestamp(
	x, tz=pytz.timezone("America/Santiago"))

def get_date_from_timezone():
	return datetime.now(tz=pytz.timezone("America/Santiago"))

def get_file_name_from_storage(name):
    if name is not None:
        name = name.split("/")
        length = len(name) - 1
        return name[length]
