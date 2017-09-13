import time
from datetime import datetime
SQL_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def format_date(date_string):
    """
    converts sql date time string to python datetime object
    """
    return  datetime.fromtimestamp(time.mktime(time.strptime(date_string,SQL_DATE_TIME_FORMAT)))
