"""A set of use specific date utilities.

This module doesn't really have a proper home yet, 
but my intention is for it to be a set of tools more 
people use in the future.

Todo:
    more date utilities!
"""
from objects import DateRangeTuple

import calendar
from datetime import (datetime, date, timedelta)

def get_prev_week_period(week_start="Monday"):
    """ Return a modified tuple containing start
    and end datetime.datetime objects.

    Examples:
        >> import date_utils
        >> dates = date_utils.get_prev_week_period()
        >> dates.start
        datetime.datetime(2017, 1, 23, 0, 0)
        >> dates.end 
        datetime.datetime(2017, 1, 29, 0, 0)

    Keyword Arguments:
        week_start (str): Day of week colloquial name. 
    """
    day_name = getattr(calendar, week_start.upper())
    now = datetime.now()
    base = datetime.strptime('%s-1-1' % (now.year), '%Y-%m-%d')
    add = 7 * (now.timetuple().tm_yday // 7 - 1) + day_name + 1
    start = base + timedelta(days=add)
    end = start + timedelta(days=6)

    return DateRangeTuple((start, end))









