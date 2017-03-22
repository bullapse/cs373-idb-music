import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artist'
    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = False)
    spotify_id = Column(String(32), nullable=False)
    image_url = Column(String(128))
    followers = Column(Integer)
    popularity = Column(Integer, nullable = False)
    genre = Column(String(32))

class Album(Base):
    __tablename__ = 'album'
    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = False)
    spotify_id = Column(String(32), nullable=False)
    image_url = Column(String(128))
    release_date = Column(Date, nullable = False)
    number_of_tracks = Column(Integer, nullable = False)
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable = False)
    popularity = Column(Integer, nullable = False)

class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = False)
    spotify_id = Column(String(32), nullable=False)
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable = False)
    album_id = Column(Integer, ForeignKey('album.id'), nullable = False)
    explicit = Column(Boolean)
    runtime = Column(Integer, nullable = False)
    popularity = Column(Integer, nullable = False)
    preview_url = Column(String(128), nullable = False)

engine = create_engine('sqlite:///cs373_idb.db')

Base.metadata.create_all(engine)
