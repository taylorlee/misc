import operator
from datetime import datetime
from pytz import utc
from dateutil.relativedelta import relativedelta

def now():
    return datetime.utcnow().replace(tzinfo=utc)

def compose_defer(opname, deferred, obj):
    class lazy(object):
        def __repr__(self):
            return 'Lazy<{op} on {obj}>'.format(
                op  = opname,
                obj = obj,
            )

    def resolve(self, other):
        op = getattr(operator, opname)
        return deferred(op(other, obj))

    for attr in ('__{}__','__r{}__'):
        setattr(lazy, attr.format(opname), resolve)

    return lazy()

class Duration(relativedelta):
    @property
    def ago(self):
        return compose_defer(
            'mul',
            lambda delta: now() - delta,
            self,
        )

    @property
    def from_now(self):
        return compose_defer(
            'mul',
            lambda delta: now() + delta,
            self,
        )

seconds  = Duration(seconds=1)
minutes  = Duration(minutes=1)
hours    = Duration(hours=1)
days     = Duration(days=1)
weeks    = Duration(weeks=1)
months   = Duration(months=1)
