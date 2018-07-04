import time
from datetime import datetime


def date2stamp(dtime):
    return time.mktime(dtime.timetuple())


def dtimeformat(dtime):
    return "{0} {1}, {2}".format(MonthString[dtime.month], dtime.day, dtime.year)


MonthString = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}
