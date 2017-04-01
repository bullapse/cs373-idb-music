#!/usr/bin/env python3
from spotify import get_playlist, get_artist, get_album, get_track
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from model import Base, Artist, Album, Track
from sqlalchemy import create_engine
from json import dumps
engine = create_engine('sqlite:///cs373_idb.db')
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


def add_track(obj):
    with session_scope() as session:
        session.add(Track(name=obj['name'],
                          spotify_id=obj['spotify_id'],
                          explicit=obj['explicit'],
                          runtime=obj['duration_ms'],
                          popularity=obj['popularity'],
                          preview_url=obj['preview_url']))


# Add all songs from lib
def add_tracks_from_playlist():
    with session_scope() as session:
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
            print(len(artists))
            for artist in artists:
                print(artist)
                artist_spotify_id = artist['id']
                print(artist_spotify_id)
                cur_artist = Artist.query.filter_by(spotify_id=artist_spotify_id).first()
                print("after query")
                if not cur_artist:
                    obj = dict()
                    obj['spotify_id'] = artist_spotify_id
                    artist_res = get_artist(artist_spotify_id)
                    obj['name'] = artist_res['name']
                    obj['image_url'] = artist_res['images'][0]['image_url'] if len(artist_res['images']) > 0 else None
                    obj['followers'] = artist_res['followers']['total']
                    obj['popularity'] = artist_res['popularity']
                    cur_artist = Artist(obj)

                # Create an Album Object
                album_spotify_id = item['track']['album']['id']
                cur_album = Album.query.filter_by(spotify_id=album_spotify_id).first()
                if not cur_album:
                    obj = dict()
                    obj['spotify_id'] = album_spotify_id
                    album_res = get_album(album_spotify_id)
                    obj['name'] = album_res['name']
                    obj['image_url'] = artist_res['images'][0]['images_url'] if len(album_res['images']) > 0 else None
                    obj['release_date'] = album_res['release_date']
                    obj['number_of_tracks'] = album_res['tracks']['total']
                    obj['popularity'] = album_res['popularity']
                    cur_album = Album(obj)

                # Create a Track Object
                track_spotify_id = item['track']['id']
                cur_track = Track.query.filter_by(spotify_id=track_spotify_id).first()
                if not cur_track:
                    obj = dict()
                    obj['spotify_id'] = track_spotify_id
                    track_res = get_track(track_spotify_id)
                    obj['name'] = track_res['name']
                    obj['spotify_id'] = track_res['spotify_id']
                    obj['explicit'] = track_res['explicit']
                    obj['runtime'] = track_res['duration_ms']
                    obj['popularity'] = track_res['popularity']
                    obj['preview_url'] = track_res['preview_url']

                cur_album.artist.append(cur_artist)
                cur_artist.albums.append(cur_album)
                cur_track.artist.append(cur_artist)
                cur_track.albums.append(cur_album)
                cur_album.tracks.append(cur_track)
                cur_artist.tracks.append(cur_track)

                # Finally add the artist object containing the albums and track
                print(cur_artist)
                session.add(cur_artist)
                session.commit()
