"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# Songs list page
app.add_url_rule('/songs', 'list_songs', view_func=views.list_songs, methods=['GET', 'POST'])

# Edit a song
app.add_url_rule('/songs/<int:song_id>/edit', 'edit_song', view_func=views.edit_song, methods=['GET', 'POST'])

# Delete a song
app.add_url_rule('/songs/<int:song_id>/delete', view_func=views.delete_song, methods=['POST'])

# Generate the song file
app.add_url_rule('/songs/<int:song_id>.wav', view_func=views.generate_song, methods=['GET'])

# Export song to JSON
app.add_url_rule('/songs/<int:song_id>.json', view_func=views.export_song, methods=['GET'])

# Import song from JSON
app.add_url_rule('/songs/import/json', view_func=views.import_song, methods=['POST'])


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

