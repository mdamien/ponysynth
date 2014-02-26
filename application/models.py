"""
models.py

App Engine datastore models

"""

from google.appengine.ext import ndb


class SongModel(ndb.Model):
    name = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=False) #song in plain-text
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
