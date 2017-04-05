from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from spotify import get_playlist, get_artist, get_album, get_track
from json import dumps

builtin_list = list

db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


artist_album_association = db.Table('artist_album_association',
    db.Column('artist_id', db.String(32), db.ForeignKey('album.id')),
    db.Column('album_id', db.String(32), db.ForeignKey('artist.id'))
)

artist_track_association = db.Table('artist_track_association',
    db.Column('artist_id', db.String(32), db.ForeignKey('track.id')),
    db.Column('track_id', db.String(32), db.ForeignKey('artist.id'))
)

album_track_association = db.Table('album_track_association',
    db.Column('album_id', db.String(32), db.ForeignKey('track.id')),
    db.Column('track_id', db.String(32), db.ForeignKey('album.id'))
)


# ---------------------- ARTISTS -------------------------- #

# [START model]
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128))
    followers = db.Column(db.Integer)
    spotify_uri = db.Column(db.String(128))
    popularity = db.Column(db.Integer, nullable=False)
    albums = db.relationship("Album", secondary=artist_album_association, backref="artist")
    tracks = db.relationship("Track", secondary=artist_track_association, backref="artist")
# [END model]


# [START list_artists]
def list_artists(limit=10, cursor=None, sort_by=None, order=None):
    # order_by = order_by if order_by else "name"
    def sort(x):
        return {
            "name": Artist.name,
            "followers": Artist.followers,
            "popularity": Artist.popularity,
        }.get(x, Artist.name)
    sort_by = sort(sort_by)
    print(sort_by)
    cursor = int(cursor) if cursor else 0
    if order:
        query = (Artist.query
                 .order_by(db.desc(sort_by))
                 .limit(limit)
                 .offset(cursor))
    else:
        query = (Artist.query
                 .order_by(sort_by)
                 .limit(limit)
                 .offset(cursor))
    artists = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(artists) == limit else None
    return (artists, next_page)
# [END list_artists]


# [START list_artists_by_track]
def list_artists_by_track(id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Artist.query.filter(Artist.tracks.any(id=id)).all())
    albums = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(albums) == limit else None
    return (albums, next_page)
# [END list_artists_by_track]


# [START list_artists_by_track_name]
def list_artists_by_track_name(name, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Artist.query.filter(Artist.tracks.any(name=name)).all())
    albums = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(albums) == limit else None
    return (albums, next_page)
# [END list_artists_by_track_name]


# [START list_artists_by_album]
def list_artists_by_album(id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Artist.query.filter(Artist.albums.any(id=id)).all())
    albums = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(albums) == limit else None
    return (albums, next_page)
# [END list_artists_by_album]


# [START list_artists_by_album_name]
def list_artists_by_album_name(name, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Artist.query.filter(Artist.albums.any(name=name)).all())
    albums = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(albums) == limit else None
    return (albums, next_page)
# [END list_artists_by_album_name]


# [START create_artist]
def create_artist(data):
    artist = Artist(**data)
    db.session.add(artist)
    db.session.commit()
    return from_sql(artist)
# [END create_artist]


# [START read_artist_id]
def read_artist(id):
    result = Artist.query.get(id)
    return from_sql(result) if result else None
# [END read_artist_id]


# [START read_artist_name]
def read_artist_name(name):
    return Artist.query.filter_by_(name=name).first()

# [END read_artist_name]


# [START update_artist]
def update_artist(data, id):
    artist = Artist.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(artist)
# [END update_artist]


def delete_artist(id):
    Artist.query.filter_by_(id=id).delete()
    db.session.commit()


# ---------------------- ALBUMS -------------------------- #

# [START model]
class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128))
    release_date = db.Column(db.Date, nullable=False)
    number_of_tracks = db.Column(db.Integer, nullable=False)
    artists = db.relationship("Artist", secondary=artist_album_association, backref="album")
    popularity = db.Column(db.Integer, nullable=False)
    tracks = db.relationship("Track", secondary=album_track_association, backref="album")
# [END model]


# [START list_albums]
def list_albums(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Album.query
             .order_by(Album.name)
             .limit(limit)
             .offset(cursor))
    albums = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(albums) == limit else None
    return (albums, next_page)
# [END list_albums]


# [START list_albums_by_artist]
def list_albums_by_artist(id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Artist.query.filter(Artist.albums.any(id=id)).all())
    albums = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(albums) == limit else None
    return (albums, next_page)
# [END list_albums_by_artist]


# [START list_albums_by_artist_name]
def list_albums_by_artist_name(name, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Artist.query.filter(Artist.albums.any(name=name)).all())
    albums = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(albums) == limit else None
    return (albums, next_page)
# [END list_albums_by_artist_name]


# [START num_albums_by_artist]
def num_albums_by_artist(name):
    return Album.query.filter(Album.artist.any(name=name)).count()
# [START num_albums_by_artist]


# [START create_album]
def create_album(data):
    album = Album(**data)
    db.session.add(album)
    db.session.commit()
    return from_sql(album)
# [END create_album]


# [START read_album]
def read_album(id):
    result = Album.query.get(id)
    return from_sql(result) if result else None
# [END read_album]


# [START update_album]
def update_album(data, id):
    album = Album.query.get(id)
    for k, v in data.items():
        setattr(album, k, v)
    db.session.commit()
    return from_sql(album)
# [END update_album]


# # [START get_number_of_albums_by_artist]
# def get_number_of_albums_by_artist(artist_id):
#     result = Album.query.filter_by(ar)
# # [END get_number_of_albums_by_artist]

def delete_album(id):
    Album.query.filter_by_(id=id).delete()
    db.session.commit()


# ---------------------- TRACKS -------------------------- #

# [START model]
class Track(db.Model):
    __tablename__ = 'track'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    spotify_uri = db.Column(db.String(128))
    artists = db.relationship("Artist", secondary=artist_track_association, backref="track")
    albums = db.relationship("Album", secondary=album_track_association, backref="track")
    explicit = db.Column(db.Boolean)
    runtime = db.Column(db.Integer, nullable=False)
    popularity = db.Column(db.Integer, nullable=False)
    preview_url = db.Column(db.String(128), nullable=True)
# [END model]


# [START list_tracks]
def list_tracks(limit=10, cursor=None, order_by=Track.name):
    cursor = int(cursor) if cursor else 0
    query = (Track.query
             .order_by(order_by)
             .limit(limit)
             .offset(cursor))
    tracks = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(tracks) == limit else None
    return (tracks, next_page)
# [END list_tracks]


# [START list_albums]
def list_tracks_by_artist(id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Track.query.filter(Track.artist.any(id=id)).all())
    tracks = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(tracks) == limit else None
    return (tracks, next_page)
# [END list_albums]


# [START list_albums]
def list_tracks_by_artist_name(name, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Track.query.filter(Track.artist.any(name=name)).all())
    tracks = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(tracks) == limit else None
    return (tracks, next_page)
# [END list_albums]


# [START list_albums]
def list_tracks_by_album(id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Track.query.filter(Track.albums.any(id=id)).all())
    tracks = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(tracks) == limit else None
    return (tracks, next_page)
# [END list_albums]


# [START list_albums]
def list_tracks_by_album_name(name, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Track.query.filter(Track.albums.any(name=name)).all())
    tracks = builtin_list(map(from_sql, query))
    next_page = cursor + limit if len(tracks) == limit else None
    return (tracks, next_page)
# [END list_albums]


# [START create_track]
def create_track(data):
    track = Track(**data)
    db.session.add(track)
    db.session.commit()
    return from_sql(track)
# [END create_album]


# [START read_track]
def read_track(id):
    result = Track.query.get(id)
    return from_sql(result) if result else None
# [END read_track]


# [START update_track]
def update_track(data, id):
    track = Track.query.get(id)
    for k, v in data.items():
        setattr(track, k, v)
    db.session.commit()
    return from_sql(track)
# [END update_track]


def delete_track(id):
    Track.query.filter_by_(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


def _load_database_from_playlist():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        pl_obj = get_playlist("Spencer")
        itterations = 0
        # print(dumps(pl_obj['tracks']['items'], indent=4, sort_keys=True))
        print(len(pl_obj['tracks']['items']))
        for item in pl_obj['tracks']['items']:
            itterations += 1
            print(itterations)
            # print(dumps(item['track'], indent=4, sort_keys=True))
            # Add all artists if they don't exist
            artists = item['track']['album']['artists']
            print("Number of artist: " + str(len(artists)))
            for artist in artists:
                artist_id = artist['id']
                cur_artist = Artist.query.filter_by(id=artist_id).first()
                if not cur_artist:
                    obj = dict()
                    obj['id'] = artist_id
                    print("artist_ID: " + artist_id)
                    artist_res = get_artist(artist_id)
                    print(dumps(artist_res, indent=4, sort_keys=True))
                    obj['name'] = artist_res['name']
                    if len(artist_res['images']) > 0:
                        obj['image_url'] = artist_res['images'][0]['url']
                    else:
                        obj['image_url'] = None
                    obj['followers'] = artist_res['followers']['total']
                    obj['popularity'] = artist_res['popularity']
                    cur_artist = Artist(**obj)

                # Create an Album Object
                album_id = item['track']['album']['id']
                cur_album = Album.query.filter_by(id=album_id).first()
                if not cur_album:
                    obj = dict()
                    obj['id'] = album_id
                    album_res = get_album(album_id)
                    obj['name'] = album_res['name']
                    if len(album_res['images']) > 0:
                        obj['image_url'] = album_res['images'][0]['url']
                    else:
                        obj['image_url'] = None
                    print(album_res['release_date'])
                    obj['release_date'] = album_res['release_date']
                    obj['number_of_tracks'] = album_res['tracks']['total']
                    obj['popularity'] = album_res['popularity']
                    cur_album = Album(**obj)

                # Create a Track Object
                track_id = item['track']['id']
                cur_track = Track.query.filter_by(id=track_id).first()
                if not cur_track:
                    obj = dict()
                    obj['id'] = track_id
                    track_res = get_track(track_id)
                    print
                    obj['name'] = track_res['name']
                    obj['id'] = track_res['id']
                    obj['explicit'] = track_res['explicit']
                    obj['runtime'] = track_res['duration_ms']
                    obj['popularity'] = track_res['popularity']
                    obj['preview_url'] = track_res['preview_url']
                    cur_track = Track(**obj)

                cur_album.artist.append(cur_artist)
                cur_artist.albums.append(cur_album)
                cur_track.artist.append(cur_artist)
                cur_track.albums.append(cur_album)
                cur_album.tracks.append(cur_track)
                cur_artist.tracks.append(cur_track)

                # Finally add the artist object containing the albums and track
                print(cur_artist)
                db.session.add(cur_artist)
                db.session.commit()


if __name__ == '__main__':
    # _create_database()
    _load_database_from_playlist()
