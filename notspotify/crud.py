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
            order = str(order)
    return token, sort, order


def get_search_args(args):
    term = request.args.get('term', None)
    # if term:
        # term = term.encode('utf-8')
    artist_token = args.get('artist_page_token', None)
    artist_sort = args.get('artist_sort', None)
    artist_order = args.get('artist_order', None)

    album_token = args.get('album_page_token', None)
    album_sort = args.get('album_sort', None)
    album_order = args.get('album_order', None)

    track_token = args.get('track_page_token', None)
    track_sort = args.get('track_sort', None)
    track_order = args.get('track_order', None)

    if artist_token:
        artist_token = artist_token.encode('utf-8')
    if artist_sort:
        artist_sort = str(artist_sort)
        if artist_order:
            artist_order = str(artist_order)

    if album_token:
        album_token = album_token.encode('utf-8')
    if album_sort:
        album_sort = str(album_sort)
        if album_order:
            album_order = str(album_order)

    if track_token:
        track_token = track_token.encode('utf-8')
    if track_sort:
        track_sort = str(track_sort)
        if track_order:
            track_order = str(track_order)

    return (term, artist_token, artist_sort, artist_order,
            album_token, album_sort, album_order,
            track_token, track_sort, track_order)


@crud.route('/search', methods=['GET'])
def search_template():
    term, artist_token, artist_sort, artist_order, album_token, album_sort, album_order, track_token, track_sort, track_order = get_search_args(request.args)

    artists, artist_cursor, artist_count, artist_limit = get_model().list_artists(term=term, cursor=artist_token, sort_by=artist_sort, order=artist_order)
    albums, album_cursor, album_count, album_limit = get_model().list_albums(term=term, cursor=album_token, sort_by=album_sort, order=album_order)
    tracks, track_cursor, track_count, track_limit = get_model().list_tracks(term=term, cursor=track_token, sort_by=track_sort, order=track_order)
    return render_template("search.html", term=term, artists=artists, artist_cursor=artist_cursor, artist_sort_by=artist_sort, artist_order=artist_order, artist_count=artist_count, artist_limit=artist_limit,
                                          albums=albums, albums_cursor=album_cursor, albums_sort_by=album_sort, albums_order=artist_order, albums_count=album_count, albums_limit=album_limit,
                                          tracks=tracks, tracks_cursor=track_cursor, tracks_sort_by=track_sort, tracks_order=track_order, tracks_count=track_count, tracks_limit=track_limit)


# ---------------------- ARTISTS -------------------------- #
# [START list_artists_template]
@crud.route('/artists', methods=['GET'])
def list_artists_template():
    token, sort, order = get_args(request.args)
    artists, cursor, count, limit = get_model().list_artists(cursor=token, sort_by=sort, order=order)
    for artist in artists:
        artist['number_of_albums'] = get_model().num_albums_by_artist(artist['id'])
        artist['number_of_tracks'] = get_model().num_tracks_by_artist(artist['id'])
    return render_template("artists.html", artists=artists, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END list_artists_template]


# [START list_artist_description_template]
@crud.route('/artist/<id>', methods=['GET'])
def list_artist_description_template(id):
    artist = get_model().read_artist(id)
    artist['number_of_albums'] = get_model().num_albums_by_artist(artist['id'])
    artist['number_of_tracks'] = get_model().num_tracks_by_artist(artist['id'])
    artist['albums'], _, _, _ = get_model().list_albums_by_artist(id)
    artist['tracks'], _, _, _ = get_model().list_tracks_by_artist(id)
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
    artists, cursor, count, limit = get_model().list_artists_by_track(id, cursor=token)
    return render_template("artists.html", artists=artists, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END list_artist_description__by_track_template]


# [START list_artist_description__by_track_name]
@crud.route('/artist/track/name/<name>', methods=['GET'])
def list_artist_description__by_track_name_template(name):
    token, sort, order = get_args(request.args)
    artists, cursor, count, limit = get_model().list_artists_by_track_name(name, cursor=token)
    return render_template("artists.html", artists=artists, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END list_artist_description__by_track_name]


# [START list_artist_description__by_album_template]
@crud.route('/artist/album/<id>', methods=['GET'])
def list_artist_description__by_album_template(id):
    token, sort, order = get_args(request.args)
    artists, cursor, count, limit = get_model().list_artists_by_album(id, cursor=token)
    return render_template("artists.html", artists=artists, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END list_artist_description__by_album_template]


# [START list_artist_description__by_album_name]
@crud.route('/artist/album/name/<name>', methods=['GET'])
def list_artist_description__by_album_name_template(name):
    token, sort, order = get_args(request.args)
    artists, cursor, count, limit = get_model().list_artists_by_album_name(name, cursor=token)
    return render_template("artists.html", artists=artists, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END list_artist_description__by_album_name]

# ---------------------- ALBUMS -------------------------- #


# [START list_albums_template]
@crud.route('/albums', methods=['GET'])
def list_albums_template():
    token, sort, order = get_args(request.args)
    albums, cursor, count, limit = get_model().list_albums(cursor=token, sort_by=sort, order=order)
    for album in albums:
        album['number_of_artists'] = get_model().get_number_of_artist_on_album(album['id'])
    return render_template("albums.html", albums=albums, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END list_albums_template]


# [START album_description_id_template]
@crud.route('/album/<id>', methods=['GET'])
def album_description_id_template(id):
    token, sort, order = get_args(request.args)
    album = get_model().read_album(id)
    artists = get_model().list_artists_by_album(id)
    tracks, _, _, _ = get_model().list_tracks_by_album(id)
    return render_template("album_description.html", album=album, tracks=tracks, artists=artistsf)
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
    albums, cursor, count, limit = get_model().list_albums_by_artist_name(name, cursor=token)
    return render_template("albums.html", albums=albums, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END albums_by_artist_name_template]


# [START albums_by_artist_template]
@crud.route('/album/artist/<id>', methods=['GET'])
def albums_by_artist_template(id):
    token, sort, order = get_args(request.args)
    albums, cursor, count, limit = get_model().list_albums_by_artist(id, cursor=token)
    return render_template("albums.html", albums=albums, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END albums_by_artist_template]

# ---------------------- TRACKS -------------------------- #


# [START list_tracks_template]
@crud.route('/tracks', methods=['GET'])
def list_tracks_template():
    token, sort, order = get_args(request.args)
    tracks, cursor, count, limit = get_model().list_tracks(cursor=token, sort_by=sort, order=order)
    return render_template("tracks.html", tracks=tracks, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END list_tracks_template]


# [START tracks_by_artist_name_template]
@crud.route('/track/artist/name/<name>')
def tracks_by_artist_name_template(name):
    token, sort, order = get_args(request.args)
    tracks, cursor, count, limit = get_model().list_tracks_by_artist_name(name)
    return render_template("tracks.html", tracks=tracks, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END tracks_by_artist_name_template]


# [START tracks_by_artist_template]
@crud.route('/track/artist/<id>')
def tracks_by_artist_template(id):
    token, sort, order = get_args(request.args)
    tracks, cursor, count, limit = get_model().list_tracks_by_artist(id)
    return render_template("tracks.html", tracks=tracks, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END tracks_by_artist_template]


# [START tracks_by_album_name_template]
@crud.route('/track/album/name/<name>')
def tracks_by_album_name_template(name):
    token, sort, order = get_args(request.args)
    tracks, cursor, count, limit = get_model().list_tracks_by_album_name(name)
    return render_template("tracks.html", tracks=tracks, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END tracks_by_album_name_template]


# [START tracks_by_album_template]
@crud.route('/track/album/<id>')
def tracks_by_album_template(id):
    token, sort, order = get_args(request.args)
    tracks, cursor, count, limit = get_model().list_tracks_by_album(id)
    return render_template("tracks.html", tracks=tracks, cursor=cursor, sort_by=sort, order=order, count=count, limit=limit)
# [END tracks_by_album_template]


# [START track_description_id_template]
@crud.route('/track/<id>')
def track_description_id_template(id):
    track = get_model().read_track(id)
    track['albums'], _, _, _ = get_model().list_albums_by_track(id)
    track['artists'], _, _, _  = get_model().list_artists_by_track(id)
    return render_template("track_description.html", track=track)
# [END track_description_id_template]


# [START track_description_id_api]
@crud.route('/track/<id>')
def track_description_id_api(id):
    track = get_model().read_track(id)
    track['albums'], _, _, _ = get_model().list_albums_by_track(id)
    track['artists'], _, _, _ = get_model().list_artists_by_track(id)
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
