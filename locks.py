'''
Quick implementation of optimistic locking on relational table rows
and pessimistic locking on external resources
'''

from django.db import models, OperationalError, IntegrityError
from contextlib import contextmanager
import time


class OptimisticallyLocked(models.Model):
    '''Model protected by concurrent updates via optimistic locking
    '''
    version = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def save(self):
        updates = {
            field.name: getattr(self, field.name)
            for field in self._meta.fields
            if not field.primary_key
        }
        updates['version'] += 1
        updated = self._meta.model.objects.filter(
            id      = self.id,
            version = self.version,
        ).update(**updates)
        if not updated:
            raise OperationalError('{} could not be updated!'.format(self))
        self.version += 1 
        return

class BankAccount(OptimisticallyLocked):
    username = models.CharField(max_length=100, unique=True)
    balance = models.IntegerField()

class PessimisticLock(models.Model):
    '''Represents a pessimistic lock on some external resource
    '''
    name = models.CharField(max_length=100, unique=True)

    @classmethod
    def acquire(cls, name):
        try:
            cls.objects.create(
                name=name,
            )
        except IntegrityError:
            raise OperationalError(
                'Could not acquire lock for: {}!'.format(name)
            )

    @classmethod
    def release(cls, name):
        cls.objects.filter(
            name=name,
        ).delete()

@contextmanager
def lock(name):
    '''prevent concurrent execution of a code block
    '''
    PessimisticLock.acquire(name)
    try:
        yield
    finally:
        PessimisticLock.release(name)
    return

def write_to_disk():
    '''example usage of locking
    '''
    with lock('diskwrite'):
        print 'WRIIIITING TO DISKKKKK'
        time.sleep(10)


