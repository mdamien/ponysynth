"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import SongForm
from models import SongModel


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    return redirect(url_for('list_songs'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username


@login_required
def list_songs():
    """List all songs"""
    songs = SongModel.query()
    form = SongForm()
    if form.validate_on_submit():
        song = SongModel(
            name=form.name.data,
            content=form.content.data,
            added_by=users.get_current_user()
        )
        try:
            song.put()
            song_id = song.key.id()
            flash(u'Song %s successfully saved.' % song_id, 'success')
            return redirect(url_for('list_songs'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_songs'))
    return render_template('list_songs.html', songs=songs, form=form)


@login_required
def edit_song(song_id):
    song = SongModel.get_by_id(song_id)
    form = SongForm(obj=song)
    if request.method == "POST":
        if form.validate_on_submit():
            song.name = form.data.get('name')
            song.content = form.data.get('content')
            song.put()
            flash(u'Song %s successfully saved.' % song_id, 'success')
            return redirect(url_for('list_songs'))
    return render_template('edit_song.html', song=song, form=form)


@login_required
def delete_song(song_id):
    song = SongModel.get_by_id(song_id)
    try:
        song.key.delete()
        flash(u'Song %s successfully deleted.' % song_id, 'success')
        return redirect(url_for('list_songs'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_songs'))

def warmup():
    return ''

