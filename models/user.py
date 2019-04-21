import jwt
from datetime import datetime, timedelta
from google.appengine.ext import ndb
from passlib.hash import pbkdf2_sha256
from settings import SECRET

class User(ndb.Model):
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def to_dict(self):
        user = {}
        user['id'] = self.key.id()
        user['name'] = self.name
        user['username'] = self.username
        user['created'] = self.created.isoformat() + 'Z'
        user['updated'] = self.updated.isoformat() + 'Z'
        return user

    @classmethod
    def save(cls, **kwargs):
        if kwargs.get('id'):
            user = cls.get_by_id(int(kwargs['id']))
        else:
            user = cls()
        if kwargs.get('name'):
            user.name = kwargs['name']
        if kwargs.get('username'):
            user.username = kwargs['username']
        if kwargs.get('password'):
            user.password = pbkdf2_sha256.hash(kwargs['password'])
        user.put()
        return user

    @classmethod
    def login(cls, username, password):
        if username and password:
            user = cls.query(cls.username == username).get()
            if user:
                if pbkdf2_sha256.verify(password, user.password):
                    user = user.to_dict()
                    user['exp'] = datetime.now() + timedelta(hours=8)
                    return jwt.encode(user, SECRET)
        return None
