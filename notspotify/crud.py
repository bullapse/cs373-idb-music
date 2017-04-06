from notspotify import get_model
from flask import Blueprint, request, render_template, jsonify

crud = Blueprint('crud', __name__)


# ========================================================== #
# ---------------------- REST API -------------------------- #
# ========================================================== #

def get_args(args):
    token = args.get('page_token', None)
    sort = args.get('sort', None)
    order = args.get('order', None)
    if token:
        token = token.encode('utf-8')
    if sort:
        sort = str(sort)
        if order:
            order = order.encode('utf-8')
    return token, sort, order


# ---------------------- ARTISTS -------------------------- #
# [START list_artists_template]
@crud.route('/artists', methods=['GET'])
def list_artists_template():
    token, sort, order = get_args(request.args)
    artists, next_page_token = get_model().list_artists(cursor=token, sort_by=sort, order=order)
    for artist in artists:
        artist['number_of_albums'] = get_model().num_albums_by_artist(artist['id'])
        artist['number_of_tracks'] = get_model().num_tracks_by_artist(artist['id'])
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artists_template]


# [START list_artist_description_template]
@crud.route('/artist/<id>', methods=['GET'])
def list_artist_description_template(id):
    artist = get_model().read_artist(id)
    artist['number_of_albums'] = get_model().num_albums_by_artist(artist['id'])
    artist['number_of_tracks'] = get_model().num_tracks_by_artist(artist['id'])
    artist['albums'], _ = get_model().list_albums_by_artist(id)
    artist['tracks'], _ = get_model().list_tracks_by_artist(id)
    print(artist['tracks'])
    return render_template("artist_description.html", artist=artist)
# [END list_artist_description_template]


# [START artist_description_name]
@crud.route('/artist/name/<name>', methods=['GET'])
def artist_description_name(name):
    artist = get_model().read_artist_name(name)
    artist['number_of_albums'] = get_model().num_albums_by_artist(artist['id'])
    artist['number_of_tracks'] = get_model().num_tracks_by_artist(artist['id'])
    return render_template("artist_description.html", artist=artist)
# [END artist_description_name]


# [START list_artist_description__by_track_template]
@crud.route('/artist/track/<id>', methods=['GET'])
def list_artist_description__by_track_template(id):
    token, sort, order = get_args(request.args)
    artists, next_page_token = get_model().list_artists_by_track(id, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artist_description__by_track_template]


# [START list_artist_description__by_track_name]
@crud.route('/artist/track/name/<name>', methods=['GET'])
def list_artist_description__by_track_name_template(name):
    token, sort, order = get_args(request.args)
    artists = get_model().list_artists_by_track_name(name, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artist_description__by_track_name]


# [START list_artist_description__by_album_template]
@crud.route('/artist/album/<id>', methods=['GET'])
def list_artist_description__by_album_template(id):
    token, sort, order = get_args(request.args)
    artists = get_model().list_artists_by_album(id, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artist_description__by_album_template]


# [START list_artist_description__by_album_name]
@crud.route('/artist/album/name/<name>', methods=['GET'])
def list_artist_description__by_album_name_template(name):
    token, sort, order = get_args(request.args)
    artists, next_page_token = get_model().list_artists_by_album_name(name, cursor=token)
    return render_template("artists.html", artists=artists, next_page_token=next_page_token)
# [END list_artist_description__by_album_name]

# ---------------------- ALBUMS -------------------------- #


# [START list_albums_template]
@crud.route('/albums', methods=['GET'])
def list_albums_template():
    token, sort, order = get_args(request.args)
    albums, next_page_token = get_model().list_albums(cursor=token, sort_by=sort, order=order)
    for album in albums:
        album['number_of_artists'] = get_model().get_number_of_artist_on_album(album['id'])
    return render_template("albums.html", albums=albums, next_page_token=next_page_token)
# [END list_albums_template]


# [START album_description_id_template]
@crud.route('/album/<id>', methods=['GET'])
def album_description_id_template(id):
    album = get_model().read_album(id)
    artists = get_model().list_artists_by_album(id)
    tracks = get_model().list_tracks_by_album(id)
    return render_template("album_description.html", album=album, tracks=tracks, artists=artists)
# [END album_description_id_template]


# [START album_description_name_template]
@crud.route('/album/name/<name>', methods=['GET'])
def album_description_name_template(name):
    album = get_model().read_album_name(name)
    return render_template("album_description.html", album=album)
# [END album_description_name_template]


# [START albums_by_artist_name_template]
@crud.route('/album/artist/name/<name>', methods=['GET'])
def albums_by_artist_name_template(name):
    token, sort, order = get_args(request.args)
    albums, next_page_token = get_model().list_albums_by_artist_name(name, cursor=token)
    return render_template("albums.html", albums=albums, next_page_token=next_page_token)
# [END albums_by_artist_name_template]


# [START albums_by_artist_template]
@crud.route('/album/artist/<id>', methods=['GET'])
def albums_by_artist_template(id):
    token, sort, order = get_args(request.args)
    albums, next_page_token = get_model().list_albums_by_artist(id, cursor=token)
    return render_template("albums.html", albums=albums, next_page_token=next_page_token)
# [END albums_by_artist_template]

# ---------------------- TRACKS -------------------------- #


# [START list_tracks_template]
@crud.route('/tracks', methods=['GET'])
def list_tracks_template():
    token, sort, order = get_args(request.args)
    tracks, next_page_token = get_model().list_tracks(cursor=token, sort_by=sort, order=order)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token, sort_by=sort, order=order)
# [END list_tracks_template]


# [START tracks_by_artist_name_template]
@crud.route('/track/artist/name/<name>')
def tracks_by_artist_name_template(name):
    token, sort, order = get_args(request.args)
    tracks, next_page_token = get_model().list_tracks_by_artist_name(name)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END tracks_by_artist_name_template]


# [START tracks_by_artist_template]
@crud.route('/track/artist/<id>')
def tracks_by_artist_template(id):
    token, sort, order = get_args(request.args)
    tracks, next_page_token = get_model().list_tracks_by_artist(id)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END tracks_by_artist_template]


# [START tracks_by_album_name_template]
@crud.route('/track/album/name/<name>')
def tracks_by_album_name_template(name):
    token, sort, order = get_args(request.args)
    tracks, next_page_token = get_model().list_tracks_by_album_name(name)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END tracks_by_album_name_template]


# [START tracks_by_album_template]
@crud.route('/track/album/<id>')
def tracks_by_album_template(id):
    token, sort, order = get_args(request.args)
    tracks, next_page_token = get_model().list_tracks_by_album(id)
    return render_template("tracks.html", tracks=tracks, next_page_token=next_page_token)
# [END tracks_by_album_template]


# [START track_description_id_template]
@crud.route('/track/<id>')
def track_description_id_template(id):
    track = get_model().read_track(id)
    track['albums'], _ = get_model().list_albums_by_track(id)
    track['artists'], _ = get_model().list_artists_by_track(id)
    return render_template("track_description.html", track=track)
# [END track_description_id_template]


# [START track_description_id_api]
@crud.route('/track/<id>')
def track_description_id_api(id):
    track = get_model().read_track(id)
    track['albums'], _ = get_model().list_albums_by_track(id)
    track['artists'], _ = get_model().list_artists_by_track(id)
    return jsonify(track)
# [END track_description_id_api]


# [START track_description_name_template]
@crud.route('/track/name/<name>')
def track_description_name_template(name):
    track = get_model().read_track_name(name)
    return render_template("track_description.html", track=track)
# [END track_description_name_template]


# [START track_description_name_api]
@crud.route('/track/name/<name>')
def track_description_name_api(name):
    track = get_model().read_track_name(name)
    return jsonify(track)
# [END track_description_name_api]
