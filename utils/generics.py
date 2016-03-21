# -*- coding: utf-8 -*-


from datetime import datetime
import pytz


tz = pytz.timezone("America/Santiago")


def timestamp_to_date(x):
    if x is not None:
        if len(str(x)) > 10:
            x = int(str(x)[0:10], base=10)
        return datetime.fromtimestamp(x, tz=tz)


def get_date_from_timezone():
    return datetime.now(tz=tz)


def get_file_name_from_storage(name):
    if name is not None:
        name = name.split("/")
        length = len(name) - 1
        return name[length]
