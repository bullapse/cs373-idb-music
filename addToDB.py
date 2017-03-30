import getSpotify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_declarative import Base, Artist, Album, Track

engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def add_artists(*ids):
    for id in ids:
        obj = get_artist(id)
        new_artist = Artist(name=obj[name],spotify_id=obj[spotify_id],image_url=obj[images][0][url], followers=obj[followers], popularity=obj[popularity])
        session.add(new_artist)
        session.commit()

def add_album(*ids):
    for id in ids:
        obj = get_album(id)
        new_album = Album(name=obj[name], spotify_id=obj[spotify_id],image_url=obj[images][0][url], release_date=obj[release_date], number_of_tracks=len(obj[tracks][items]), artist_id=obj[artists][id], popularity=obj[popularity])
        session.add(new_album)
        session.commit()

def add_tracks(*ids):
    for id in ids:
        obj = get_track(id)
        # need to add artist and album name to the getSpotify.get_track function
        new_track = Track(name=obj[name],spotify_id=obj[spotify_id], explicit=obj[explicit], runtime=obj[duration_ms], popularity=obj[popularity], preview_url=obj[preview_url])
        session.add(new_track)
        session.commit()
