"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, send_file, jsonify

from application import app
from decorators import login_required, admin_required
from forms import SongForm, ImportForm
from models import SongModel

import song_parser
from synth import make_wav
import StringIO
import json

def home():
    return redirect(url_for('list_songs'))

@login_required
def list_songs():
    """List all songs"""
    import_form = ImportForm()
    songs_unfiltered = SongModel.query()
    songs = [song for song in songs_unfiltered if song.added_by == users.get_current_user()]
    
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
    return render_template('list_songs.html', songs=songs, form=form, import_form=import_form)


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

@login_required
def generate_song(song_id):
    file_ = StringIO.StringIO()
    song = SongModel.get_by_id(song_id)
    parsed_song = song_parser.parse(song.content)
    make_wav(parsed_song,fn=file_)
    file_.seek(0)
    return send_file(file_, attachment_filename="%s.wav" % song_id,as_attachment=True)

@login_required
def export_song(song_id):
    song = SongModel.get_by_id(song_id)
    return jsonify(name=song.name,content=song.content)

@login_required
def import_song():
    form = ImportForm()
    if form.validate_on_submit():
        song_json = json.loads(request.files[form.json.name].read())
        name = song_json.get('name')
        content = song_json.get('content')
        song = SongModel(name=name,content=content,added_by=users.get_current_user())
        try:
            song.put()
            song_id = song.key.id()
            flash(u'Song %s successfully saved.' % song_id, 'success')
            return redirect(url_for('list_songs'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_songs'))
        return redirect(url_for('list_songs'))

def warmup():
    return ''

