#!/usr/bin/env python3

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from model import Base, Artist, Album, Track

engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

class TestNetflix (TestCase):

    def test_case_1(self):
        new_artist = Artist(name='test',spotify_id='1',image_url='test.png', followers=0, popularity=0)
        session.add(new_artist)
        session.commit()
        self.assertEqual(new_artist, session.query(Artist).first())

    def test_case_2(self):
        new_album = Album(name='test', spotify_id='2',image_url='test.png', release_date='2017-3-22', number_of_tracks=10, artist_id=1, popularity=10)
        session.add(new_album)
        session.commit()
        self.assertEqual(new_artist, session.query(Album).first())

    def test_case_3(self):
        new_track = Track(name='test',spotify_id='3', explicit=True, runtime=200000, popularity=50, preview_url='test.mp3')
        session.add(new_track)
        session.commit()
        self.assertEqual(new_artist, session.query(Track).first())

    def test_case_4(self):
        artist = session.query(Artist).first()
        self.assertEqual(new_artist.id, '1')

    def test_case_5(self):
        artist = session.query(Album).first()
        self.assertEqual(new_album.id, '2')

    def test_case_6(self):
        artist = session.query(Track).first()
        self.assertEqual(new_album.id, '3')

    def test_case_7(self):
        new_artist = Artist(name='test',spotify_id='1',image_url='test.png', followers=0, popularity=0)
        session.delete(new_artist)
        session.commit()
        self.assertTrue(session.query(Artist).first() is None)

    def test_case_8(self):
        new_album = Album(name='test', spotify_id='2',image_url='test.png', release_date='2017-3-22', number_of_tracks=10, artist_id=1, popularity=10)
        session.delete(new_album)
        session.commit()
        self.assertTrue(session.query(Album).first() is None)

    def test_case_9(self):
        new_track = Track(name='test',spotify_id='3', explicit=True, runtime=200000, popularity=50, preview_url='test.mp3')
        session.delete(new_track)
        session.commit()
        self.assertTrue(session.query(Track).first() is None)


if __name__ == "__main__":
    main()
