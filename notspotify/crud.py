from notspotify import get_model
from flask import Blueprint, render_template, request
import spotify
import requests

ACCESS_TOKEN = None
CLIENT_ID = '78237eb54be441c7bafdf02459e9d5ad'
CLIENT_SECRET = '3cde3d481c8b432ba6800e80412722a9'
AUTH_HEADER = 'NzgyMzdlYjU0YmU0NDFjN2JhZmRmMDI0NTllOWQ1YWQ6M2NkZTNkNDgxYzhiNDMyYmE2ODAwZTgwNDEyNzIyYTk='
SCOPE = "playlist-read-private"

crud = Blueprint('crud', __name__)


# ========================================================== #
# ---------------------- REST API -------------------------- #
# ========================================================== #

# [START list_artists]
@crud.route('/artists', methods=['GET'])
def list_artists():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    artists, next_page_token = get_model().list_artists(cursor=token)

    return render_template(
        "artist.html",
        artists=artists,
        next_page_token=next_page_token)
# [END list_artists]


# [START list_artist_description_id]
@crud.route('/artist/<id>')
def list_artist_description_id(id):
    artist = get_model().read_artist_id(id)
    return render_template("artist_description.html", artist=artist)
# [END list_artist_description_id]


# [START artist_description_name]
@crud.route('/artist/name/<name>')
def artist_description_name(name):
    artist = get_model().read_artist_name(name)
    return render_template("artist_description.html", artist=artist)
# [END artist_description_name]


# [START albums]
@crud.route('/albums', methods=['GET'])
def list_albums():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    albums, next_page_token = get_model().list_artists(cursor=token)

    return render_template(
        "albums.html",
        albums=albums,
        next_page_token=next_page_token)
# [END list_albums]


# [START album_description_id]
@crud.route('/album/<id>')
def album_description_id(id):
    album = get_model().read_album_id(id)
    return render_template("album_description.html", album=album)
# [END album_description_id]


# [START album_description_name]
@crud.route('/album/name/<name>')
def album_description_name(name):
    album = get_model().read_album_name(name)
    return render_template("album_description.html", album=album)
# [END album_description_name]

# [START list_tracks]
@crud.route('/tracks', methods=['GET'])
def list_tracks():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    albums, next_page_token = get_model().list_artists(cursor=token)

    return render_template(
        "tracks.html",
        tracks=tracks,
        next_page_token=next_page_token)
# [END list_tracks]


# [START album_description_id]
@crud.route('/tracks/<id>')
def track_description_id(id):
    track = get_model().read_album_id(id)
    return render_template("album_description.html", track=track)
# [END album_description_id]


# [START album_description_name]
@crud.route('/tracks/name/<name>')
def track_description_name(name):
    track = get_model().read_album_name(name)
    return render_template("album_description.html", track=track)
# [END album_description_name]
