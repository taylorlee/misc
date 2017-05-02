import operator
from datetime import datetime
from dateutil.relativedelta import relativedelta

def __mul__(self, other):
    try:
        f = float(other)
    except TypeError:
        return NotImplemented
    return relativedelta(
        years        = int(self.years*f)        ,
        months       = int(self.months*f)       ,
        days         = int(self.days*f)         ,
        hours        = int(self.hours*f)        ,
        minutes      = int(self.minutes*f)      ,
        seconds      = int(self.seconds*f)      ,
        microseconds = int(self.microseconds*f) ,
        leapdays     = self.leapdays            ,
        year         = self.year                ,
        month        = self.month               ,
        day          = self.day                 ,
        weekday      = self.weekday             ,
        hour         = self.hour                ,
        minute       = self.minute              ,
        second       = self.second              ,
        microsecond  = self.microsecond         ,
     )

relativedelta.__mul__  = __mul__
relativedelta.__rmul__ = __mul__

class TimeShift(object):
    def __init__(self, op):
        self.op = op

    def __mul__(self, other):
        return self.op(datetime.now(), other)
    __rmul__ = __mul__

seconds  = relativedelta(seconds=1)
minutes  = relativedelta(minutes=1)
hours    = relativedelta(hours=1)
days     = relativedelta(days=1)
weeks    = relativedelta(weeks=1)
months   = relativedelta(months=1)

ago      = TimeShift(operator.sub) 
from_now = TimeShift(operator.add)
