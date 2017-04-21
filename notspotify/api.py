from notspotify import get_model
from flask import Blueprint, request, jsonify

API_VERSION = 'v1'
api = Blueprint('api', __name__)


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

# [START list_artist_api]
@api.route('/api/' + API_VERSION + '/artists', methods=['GET'])
def list_artist_api():
    token, sort, order = get_args(request.args)
    artists, cursor, _, limit = get_model().list_artists(cursor=token, sort_by=sort, order=order)
    for artist in artists:
        artist['number_of_albums'] = get_model().num_albums_by_artist(artist['id'])
        artist['number_of_tracks'] = get_model().num_tracks_by_artist(artist['id'])
    return jsonify([artists, (cursor + limit)])
# [END list_artist_api]


# [START list_artist_description_api]
@api.route('/api/' + API_VERSION + '/artist/<id>', methods=['GET'])
def list_artist_description_api(id):
    artist = get_model().read_artist(id)
    artist['number_of_albums'] = get_model().num_albums_by_artist(artist['id'])
    artist['number_of_tracks'] = get_model().num_tracks_by_artist(artist['id'])
    artist['albums'], _ = get_model().list_albums_by_artist(id)
    artist['tracks'], _ = get_model().list_tracks_by_artist(id)
    return jsonify(artist)
# [END list_artist_description_api]


# [START list_artist_description__by_track_api]
@api.route('/api/' + API_VERSION + '/artist/track/<id>', methods=['GET'])
def list_artist_description__by_track_api(id):
    token, sort, order = get_args(request.args)
    artists, cursor, _, limit = get_model().list_artists_by_track(id, cursor=token)
    return jsonify([artists, (cursor + limit)])
# [END list_artist_description__by_track_api]


# [START list_artist_description__by_album_api]
@api.route('/api/' + API_VERSION + '/artist/album/<id>', methods=['GET'])
def list_artist_description__by_album_api(id):
    artists = get_model().list_artists_by_album(id)
    print(artists)
    return jsonify(artists)
# [END list_artist_description__by_album_api]

# ---------------------- ALBUMS -------------------------- #


# [START list_albums_api]
@api.route('/api/' + API_VERSION + '/albums', methods=['GET'])
def list_albums_api():
    token, sort, order = get_args(request.args)
    albums, cursor, _, limit = get_model().list_albums(cursor=token, sort_by=sort, order=order)
    for album in albums:
        album['number_of_artists'] = get_model().get_number_of_artist_on_album(album['id'])
        album['artists'] = get_model().list_artists_by_album(album['id'])
        album['tracks'] = get_model().list_tracks_by_album(album['id'])
    return jsonify([albums, (cursor + limit)])
# [END list_albums_api]


# [START album_description_id_api]
@api.route('/api/' + API_VERSION + '/album/<id>', methods=['GET'])
def album_description_id_api(id):
    album = get_model().read_album(id)
    artists = get_model().list_artists_by_album(id)
    tracks = get_model().list_tracks_by_album(id)
    album['artists'] = artists
    album['tracks'] = tracks
    return jsonify(album)
# [END album_description_id_api]


# [START albums_by_artist_api]
@api.route('/api/' + API_VERSION + '/album/artist/<id>', methods=['GET'])
def albums_by_artist_api(id):
    token, sort, order = get_args(request.args)
    albums, cursor, _, limit = get_model().list_albums_by_artist(id, cursor=token)
    for album in albums:
        artists = get_model().list_artists_by_album(album['id'])
        tracks, _ = get_model().list_tracks_by_album(album['id'])
        album['artists'] = artists
        album['tracks'] = tracks
    return jsonify([albums, (cursor + limit)])
# [END albums_by_artist_api]

# ---------------------- TRACKS -------------------------- #


# [START list_tracks_api]
@api.route('/api/' + API_VERSION + '/tracks', methods=['GET'])
def list_tracks_api():
    token, sort, order = get_args(request.args)
    tracks, cursor, _, limit = get_model().list_tracks(cursor=token, sort_by=sort, order=order)
    return jsonify([tracks, (cursor + limit)])
# [END list_tracks_api]


# [START tracks_by_artist_api]
@api.route('/api/' + API_VERSION + '/track/artist/<id>')
def tracks_by_artist_api(id):
    token, sort, order = get_args(request.args)
    tracks, cursor, _, limit = get_model().list_tracks_by_artist(id)
    return jsonify([tracks, (cursor + limit)])
# [END tracks_by_artist_api]


# [START tracks_by_album_api]
@api.route('/api/' + API_VERSION + '/track/album/<id>')
def tracks_by_album_api(id):
    token, sort, order = get_args(request.args)
    tracks, cursor, _, limit = get_model().list_tracks_by_album(id)
    return jsonify([tracks, (cursor + limit)])
# [END tracks_by_album_api]


# [START track_description_id_api]
@api.route('/api/' + API_VERSION + '/track/<id>')
def track_description_id_api(id):
    track = get_model().read_track(id)
    track['albums'], _ = get_model().list_albums_by_track(id)
    track['artists'], _ = get_model().list_artists_by_track(id)
    return jsonify(track)
# [END track_description_id_api]
