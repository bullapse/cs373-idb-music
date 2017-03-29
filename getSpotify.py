#!/usr/bin/env python3

# ------------------------------
# projects/collatz/RunCollatz.py
# Copyright (C) 2017
# Spencer Bull
# ------------------------------

# -------
# imports
# -------

from requests import get

CLIENT_ID = "78237eb54be441c7bafdf02459e9d5ad"
CLIENT_SECRET = "3cde3d481c8b432ba6800e80412722a9"

ARTISTS = ["4LZ4De2MoO3lP6QaNCfvcu",
           "62Jfwxon19ZOT9eSL6bvtY",
           "2cFrymmkijnjDg9SS92EPM"]
ALBUMS = ["6S0sbdQmuF3IhNRcMkuQK3",
          "4w0aS3VhSU7QHEN4zfpvHv",
          "41B7cBcRZDSE62bo0eoBTW"]
TRACKS = ["1OcHQQ7A239YbKqKBYw2yw",
          "2BvI93upqv44QI4hVTvAC3",
          "53wXk7sMOnvkdAcEpGzu8W"]

PLAYLISTS = [{
    "user": "Spencer",
    "user_id": "1229502046",
    "playlist_id": "2GejolY4BJCsbUxf0yPydq"
}]

# ----------
# auth
# ----------


def auth():
    res = get('https://accounts.spotify.com/authorize?client_id=' + CLIENT_ID + '&response_type=code&redirect_uri=https%3A%2F%2Fnotspotify.me%2Fspotfiycallback')
    return ret_obj


# ----------
# get_artist
# ----------


def get_artist():
    ret_obj = []
    for spotify_id in ARTISTS:
        response = get('https://api.spotify.com/v1/artists/' + spotify_id)
        res = response.json()
        obj = {}
        obj['id'] = 42  # TODO: remove
        obj['name'] = ['name']
        obj['spotify_id'] = res['id']
        obj['images'] = res['images']
        obj['popularity'] = res['popularity']
        obj['uri'] = res['uri']
        obj['followers'] = res['followers']
        ret_obj.append(obj)
    return ret_obj


# ----------
# get_album
# ----------


def get_album():
    ret_obj = []
    for spotify_id in ALBUMS:
        response = get('https://api.spotify.com/v1/albums/' + spotify_id)
        res = response.json()
        obj = {}
        obj['id'] = 42  # TODO: remove
        obj['name'] = res['name']
        obj['spotify_id'] = res['id']
        obj['images'] = res['images']
        obj['popularity'] = res['popularity']
        obj['uri'] = res['uri']
        obj['artists'] = res['artists']
        obj['copyrights'] = res['copyrights']
        obj['external_ids'] = res['external_ids']
        obj['external_urls'] = res['external_urls']
        obj['genres'] = res['genres']
        obj['href'] = res['href']
        obj['release_date'] = res['release_date']
        obj['release_date_precision'] = res['release_date_precision']
        obj['tracks'] = res['tracks']
        obj['spotif_uri'] = res['uri']
        ret_obj.append(obj)
    return ret_obj


# ----------
# get_artist
# ----------


def get_track():
    ret_obj = []
    for spotify_id in TRACKS:
        response = get('https://api.spotify.com/v1/tracks/' + spotify_id)
        res = response.json()
        obj = {}
        obj['id'] = 42  # TODO: remove
        obj['name'] = res['name']
        obj['spotify_id'] = res['id']
        obj['duration_ms'] = res['duration_ms']
        obj['popularity'] = res['popularity']
        obj['uri'] = res['uri']
        obj['explicit'] = res['explicit']
        obj['external_urls'] = res['external_urls']
        obj['href'] = res['href']
        obj['preview_url'] = res['preview_url']
        obj['spotify_uri'] = res['uri']
        ret_obj.append(obj)
    return ret_obj


# ------------
# get_playlist
# ------------


def get_playlist(user):
    ret = {}
    pl_info = (next(pl for pl in PLAYLISTS if pl['user'] == user), None)[0]
    print(pl_info)
    if pl_info is not None:
        url = 'https://api.spotify.com/v1/users/' + pl_info['user_id'] + '/playlists/' + pl_info['playlist_id']
        print(url)
        res = get(url)
        ret['followers'] = res['followers']
        ret['description'] = res['description']
        ret['images'] = res['images']
        ret['owner'] = res['owner']
        ret['tracks'] = res['tracks']
    return ret
