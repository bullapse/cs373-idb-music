from notspotify import get_model
from flask import Blueprint, request, render_template

crud = Blueprint('crud', __name__)


# ========================================================== #
# ---------------------- REST API -------------------------- #
# ========================================================== #

# ---------------------- ARTISTS -------------------------- #
# [START list_artists]
@crud.route('/artists', methods=['GET'])
def list_artists():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    artists, next_page_token = get_model().list_artists(cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artists]


# [START list_artist_description_id]
@crud.route('/artist/<id>', methods=['GET'])
def list_artist_description(id):
    artist = get_model().read_artist(id)
    return render_template("artist_description.html", artist=artist)
# [END list_artist_description_id]


# [START artist_description_name]
@crud.route('/artist/name/<name>', methods=['GET'])
def artist_description_name(name):
    artist = get_model().read_artist_name(name)
    return render_template("artist_description.html", artist=artist)
# [END artist_description_name]


# [START list_artist_description_id]
@crud.route('/artist/track/<id>', methods=['GET'])
def list_artist_description__by_track(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    artists = get_model().list_artists_by_track(id, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artist_description_id]


# [START artist_description_name]
@crud.route('/artist/track/name/<name>', methods=['GET'])
def list_artist_description__by_track_name(name):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    artists = get_model().list_artists_by_track_name(name, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END artist_description_name]


# [START list_artist_description_id]
@crud.route('/artist/album/<id>', methods=['GET'])
def list_artist_description__by_album(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    artists = get_model().list_artists_by_album(id, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artist_description_id]


# [START artist_description_name]
@crud.route('/artist/album/name/<name>', methods=['GET'])
def list_artist_description__by_album_name(name):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    artists = get_model().list_artists_by_album_name(name, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END artist_description_name]

# ---------------------- ALBUMS -------------------------- #


# [START albums]
@crud.route('/albums', methods=['GET'])
def list_albums():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    albums = get_model().list_artists(cursor=token)
    return render_template("albums.html", albums=albums, next_page_token=next_page_token)
# [END list_albums]


# [START album_description_id]
@crud.route('/album/<id>', methods=['GET'])
def album_description_id(id):
    album = get_model().read_album_id(id)
    return render_template("album_description.html", album=album)
# [END album_description_id]


# [START album_description_name]
@crud.route('/album/name/<name>', methods=['GET'])
def album_description_name(name):
    album = get_model().read_album_name(name)
    return render_template("album_description.html", album=album)
# [END album_description_name]


# [START album_description_name]
@crud.route('/album/artist/name/<name>', methods=['GET'])
def albums_by_artist_name(name):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    albums, next_page_toke = get_model().list_albums_by_artist_name(name, cursor=token)
    return render_template("albums.html", albums=albums, next_page_token=next_page_token)
# [END album_description_name]


# [START album_description_name]
@crud.route('/album/artist/<id>', methods=['GET'])
def albums_by_artist(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    albums = get_model().list_albums_by_artist(id, cursor=token)
    return render_template("albums.html", albums=albums, next_page_token=next_page_token)
# [END album_description_name]

# ---------------------- TRACKS -------------------------- #


# [START list_tracks]
@crud.route('/tracks', methods=['GET'])
def list_tracks():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    tracks, next_page_token = get_model().list_artists(cursor=token)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END list_tracks]


# [START album_description_name]
@crud.route('/track/artist/name/<name>')
def tracks_by_artist_name(name):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    tracks, next_page_token = get_model().list_tracks_by_artist_name(name)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END album_description_name]


# [START album_description_name]
@crud.route('/track/artist/<id>')
def tracks_by_artist(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    tracks, next_page_token = get_model().list_tracks_by_artist(id)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END album_description_name]


# [START album_description_name]
@crud.route('/track/album/name/<name>')
def tracks_by_album_name(name):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    tracks, next_page_token = get_model().list_tracks_by_album_name(name)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END album_description_name]


# [START album_description_name]
@crud.route('/track/album/<id>')
def tracks_by_album(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    tracks, next_page_token = get_model().list_tracks_by_album(id)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END album_description_name]


# [START album_description_id]
@crud.route('/tracks/<id>')
def track_description_id(id):
    track = get_model().read_album_id(id)
    return render_template("track_description.html", track=track)
# [END album_description_id]


# [START album_description_name]
@crud.route('/tracks/name/<name>')
def track_description_name(name):
    track = get_model().read_album_name(name)
    return render_template("track_description.html", track=track)
# [END album_description_name]
