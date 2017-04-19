'''Quick implementation of optimistic locking on relational tables
'''

from django.db import models, OperationalError

class OptimisticLock(models.Model):
    version = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def update_field(self, field, value):
        new_version = self.version+1
        updated = self._meta.model.objects.filter(
            id      = self.id,
            version = self.version,
        ).update(**{
            field     : value,
            'version' : new_version,
        })
        if not updated:
            raise OperationalError('{} could not be updated!'.format(self))
        self.version = new_version
        setattr(self, field, value)
        return

class Bank(OptimisticLock):
    value = models.IntegerField()

class DiskWrite(OptimisticLock):
    in_progress = models.BooleanField()

import time
def write_to_disk():
    try:
        lock = DiskWrite.objects.filter(
            in_progress=False,
        ).get()
    except DiskWrite.DoesNotExist:
        raise OperationalError('Could not acquire lock!')
    lock.update_field('in_progress', True)

    print 'WRIIIITING TO DISKKKKK'

    time.sleep(10)
    lock.update_field('in_progress',False)


