'''python date functions inspired by rails' 1.day.ago


Example:
In [1]: from numerals import *

In [2]: one.day.ago + two.days
Out[2]: datetime.datetime(2017, 4, 18, 13, 30, 32, 490872)
'''

import operator
from datetime import timedelta, datetime

class Past(object):
    def __get__(self, obj, objtype):
        return datetime.now() - obj

class Future(object):
    def __get__(self, obj, objtype):
        return datetime.now() + obj

class RelativeTime(object):
    ago = Past()
    from_now = Future()

    def __init__(self, multiplier):
        self.scale = multiplier

    def __get__(self, obj, objtype):
        self.product = self.scale * obj.val
        return self
    
    @property
    def as_delta(self):
        return timedelta(days=self.product)

    def _left_op(self, other, op):
        if isinstance(other, type(self)):
            delta = other.as_delta
        elif isinstance(other, timedelta):
            delta = other
        else:
            raise NotImplemented
        return op(self.as_delta, delta)

    def __add__(self, other):
        return self._left_op(other, operator.add)

    def __sub__(self, other):
        return self._left_op(other, operator.sub)

    def _right_op(self, other, op):
        if isinstance(other, datetime):
            return op(other, self.as_delta)
        else:
            raise NotImplemented

    def __radd__(self, other):
        return self._right_op(other, operator.add)

    def __rsub__(self, other):
        return self._right_op(other, operator.sub)


class Numeral(object):
    days = RelativeTime(1)
    weeks = RelativeTime(7)
    # month = RelativeMonth() # TODO use relativedelta

    def __init__(self, val):
        self.val = val

class One(object):
    day = RelativeTime(1)
    week = RelativeTime(7)
    val = 1

zero      = Numeral(0)

one       = One()
two       = Numeral(2)
three     = Numeral(3)
four      = Numeral(4)
five      = Numeral(5)
six       = Numeral(6)
seven     = Numeral(7)
eight     = Numeral(8)
nine      = Numeral(9)

ten       = Numeral(10)
eleven    = Numeral(11)
twelve    = Numeral(12)
thirteen  = Numeral(13)
fourteen  = Numeral(14)
fifteen   = Numeral(15)
sixteen   = Numeral(16)
seventeen = Numeral(17)
eighteen  = Numeral(18)
nineteen  = Numeral(19)

#twenty
#thirty
#fourty
#fifty
#sixty
#seventy
#eighty
#ninety
