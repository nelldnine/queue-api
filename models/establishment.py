from google.appengine.ext import ndb

class Establishment(ndb.Model):
    name = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def to_dict(self):
        establishment = {}
        establishment['id'] = self.key.id()
        establishment['name'] = self.name
        establishment['created'] = self.created.isoformat() + 'Z'
        establishment['updated'] = self.updated.isoformat() + 'Z'
        return establishment

    @classmethod
    def save(cls, **kwargs):
        if kwargs.get('id'):
            establishment = cls.get_by_id(int(kwargs['id']))
        else:
            establishment = cls()
        if kwargs.get('name'):
            establishment.name = kwargs['name']
        establishment.put()
        return establishment
