#!/usr/bin/env python3

from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy_declarative import Base, Artist, Album, Track
from sqlalchemy import create_engine
engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def add_artist(obj):
    with session_scope() as session:
        session.add(Artist(name=obj['name'],
                           spotify_id=obj['spotify_id'],
                           image_url=obj['images'][0]['url'],
                           followers=obj['followers'],
                           popularity=obj['popularity']))


def add_album(obj):
    with session_scope() as session:
        session.add(Album(name=obj['name'],
                          spotify_id=obj['spotify_id'],
                          image_url=obj['images'][0]['url'],
                          release_date=obj['release_date'],
                          number_of_tracks=len(obj['tracks']['items']),
                          artist_id=obj['artists']['id'],
                          popularity=obj['popularity']))


def add_tracks(obj):
    with session_scope() as session:
        session.add(Track(name=obj['name'],
                          spotify_id=obj['spotify_id'],
                          explicit=obj['explicit'],
                          runtime=obj['duration_ms'],
                          popularity=obj['popularity'],
                          preview_url=obj['preview_url']))
