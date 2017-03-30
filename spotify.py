#!/usr/bin/env python3

# ------------------------------
# projects/collatz/RunCollatz.py
# Copyright (C) 2017
# Spencer Bull
# ------------------------------

# -------
# imports
# -------

import sys

import requests

ARTISTS = ["4LZ4De2MoO3lP6QaNCfvcu", "62Jfwxon19ZOT9eSL6bvtY", "2cFrymmkijnjDg9SS92EPM"]
ALBUMS = ["6S0sbdQmuF3IhNRcMkuQK3", "4w0aS3VhSU7QHEN4zfpvHv", "41B7cBcRZDSE62bo0eoBTW"]
TRACKS = ["1OcHQQ7A239YbKqKBYw2yw", "2BvI93upqv44QI4hVTvAC3", "53wXk7sMOnvkdAcEpGzu8W"]


# ---------------
# init_database
# ---------------

def init_database():
    return False


# ----------
# get_artist
# ----------


def get_artist():
    ret_obj = []
    for spotify_id in ARTISTS:
        response = requests.get('https://api.spotify.com/v1/artists/' + spotify_id)
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
    response = requests.get('https://api.spotify.com/v1/albums/' + spotify_id)
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
    response = requests.get('https://api.spotify.com/v1/tracks/' + spotify_id)
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
