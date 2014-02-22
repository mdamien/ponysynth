"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import SongModel


class ClassicSongForm(wtf.Form):
    name = wtf.TextField('Name', validators=[validators.Required()])
    content = wtf.TextAreaField('Song', validators=[validators.Required()])

class ImportForm(wtf.Form):
    json = wtf.FileField('Import song:', validators=[validators.Required()])

# App Engine ndb model form song
SongForm = model_form(SongModel, wtf.Form, field_args={
    'name': dict(validators=[validators.Required()]),
    'content': dict(validators=[validators.Required()]),
})
