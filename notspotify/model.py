from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

builtin_list = list

db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['sppotify_id'] = row.spotify_id
    data.pop('_sa_instance_state')
    return data


Base = declarative_base()

album_artist_association = db.Table('album_artist_association', Base.metadata,
    db.Column('artist_spotify_id', db.String, db.ForeignKey('album_spotify_id')),
    db.Column('album_spotify_id', db.String, db.ForeignKey('artist_spotify_id')),
)

artist_track_association = db.Table('track_artist_association', Base.metadata,
    db.Column('track_spotify_id', db.String, db.ForeignKey('artist_sptoify_id')),
    db.Column('artist_spotify_id', db.String, db.ForeignKey('track_spotify_id'))
)

album_track_association = db.Table('album_track_association', Base.metadata,
    db.Column('album_spotify_id', db.String, db.ForeignKey('track_spotify_id')),
    db.Column('track_spotfiy_id', db.String, db.ForeignKey('album_spotify_id'))
)


# [START model]
class Artist(db.Model):
    __tablename__ = 'artist'

    spotify_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128))
    followers = db.Column(db.Integer)
    popularity = db.Column(db.Integer, nullable=False)
    albums = relationship("Album", secondary=album_artist_association, backref="album")
    tracks = relationship("Track", secondary=artist_track_association, backref="track")
# [END model]


# [START list_artists]
def list_artists(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Artist.query
             .order_by(Artist.name)
             .limit(limit)
             .offset(cursor))
    artists = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(artists) == limit else None
    return (artists, next_page)
# [END list_artists]


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


# [START model]
class Album(db.Model):
    __tablename__ = 'album'

    spotify_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128))
    release_date = db.Column(db.Date, nullable=False)
    number_of_tracks = db.Column(db.Integer, nullable=False)
    artists = relationship("Artist", secondary=album_artist_association, backref="artist")
    popularity = db.Column(db.Integer, nullable=False)
    tracks = relationship("Track", secondary=album_track_association, backref="track")
# [END model]


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


def delete_album(id):
    Album.query.filter_by_(id=id).delete()
    db.session.commit()


# [START model]
class Track(db.Model):
    __tablename__ = 'track'

    spotify_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    artists = relationship("Artist", secondary=artist_track_association, backref="artist")
    albums = relationship("Album", secondary=album_track_association, backref="album")
    explicit = db.Column(db.Boolean)
    runtime = db.Column(db.Integer, nullable=False)
    popularity = db.Column(db.Integer, nullable=False)
    preview_url = db.Column(db.String(128), nullable=False)
# [END model]


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


if __name__ == '__main__':
    _create_database()
