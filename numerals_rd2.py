import operator
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd

class relativedelta(rd):
    def __mul__(self, other):
        try:
            rd2 = super(relativedelta, self).__mul__(other)
        except TypeError:
            return NotImplemented
        return relativedelta(**{
            k:v
            for k,v in vars(rd2).items()
            if not k.startswith('_')
        })
        
    __rmul__ = __mul__

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
