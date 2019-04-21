import string
import random
from google.appengine.ext import ndb

def id_generator(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Counter(ndb.Model):
    establishment = ndb.KeyProperty()
    auth_key = ndb.StringProperty()
    number = ndb.IntegerProperty(default=1)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def to_dict(self):
        counter = {}
        counter['id'] = self.key.id()
        counter['number'] = self.number
        counter['created'] = self.created.isoformat() + 'Z'
        counter['updated'] = self.updated.isoformat() + 'Z'
        return counter

    def step_up(self):
        self.number += 1
        self.auth_key = id_generator()
        self.put()
        return self.to_dict()

    @classmethod
    def save(cls, **kwargs):
        if kwargs.get('id'):
            counter = cls.get_by_id(int(kwargs['id']))
        else:
            counter = cls()
        if kwargs.get('establishment'):
            counter.establishment = ndb.Key('Establishment', kwargs['establishment'])
        counter.auth_key = id_generator()
        counter.put()
        return counter
