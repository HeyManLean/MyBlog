import time
from datetime import datetime


def date2stamp(dtime):
    return time.mktime(dtime.timetuple())
