#!/usr/bin/env python3

# ------------------------------
# projects/collatz/RunCollatz.py
# Copyright (C) 2017
# Spencer Bull
# ------------------------------

# -------
# imports
# -------

import requests
# import requests_toolbelt.adapters.appengine
#
# # Use the App Engine Requests adapter. This makes sure that Requests uses
# # URLFetch.
# requests_toolbelt.adapters.appengine.monkeypatch()


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

SCOPE = "playlist-read-private"
ACCESS_TOKEN = None
AUTH_HEADER = 'NzgyMzdlYjU0YmU0NDFjN2JhZmRmMDI0NTllOWQ1YWQ6M2NkZTNkNDgxYzhiNDMyYmE2ODAwZTgwNDEyNzIyYTk='

# ----------
# auth
# ----------


def auth():
    global ACCESS_TOKEN
    url = 'https://accounts.spotify.com/api/token'
    body = {
    	'grant_type': 'client_credentials'
    }
    res = requests.post(url, data=body, auth=requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    ACCESS_TOKEN = res.json()['access_token']
    return ACCESS_TOKEN


# ----------
# get_artist
# ----------


def get_artist(id):
    response = requests.get('https://api.spotify.com/v1/artists/' + id)
    # response.raise_for_status()
    res = response.json()
    obj = {}
    obj['name'] = res['name']
    obj['id'] = res['id']
    obj['images'] = res['images']
    obj['popularity'] = res['popularity']
    obj['uri'] = res['uri']
    obj['followers'] = res['followers']
    return obj


# ----------
# get_album
# ----------


def get_album(id):
    response = requests.get('https://api.spotify.com/v1/albums/' + id)
    # response.raise_for_status()
    res = response.json()
    obj = {}
    obj['name'] = res['name']
    obj['id'] = res['id']
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
    if len(obj['release_date']) < 5:
        obj['release_date'] = res['release_date'] + '-01-01'
    obj['release_date_precision'] = res['release_date_precision']
    obj['tracks'] = res['tracks']
    obj['spotif_uri'] = res['uri']
    return obj


# ----------
# get_artist
# ----------

def get_track(id):
    response = requests.get('https://api.spotify.com/v1/tracks/' + id)
    # response.raise_for_status()
    res = response.json()
    obj = {}
    obj['name'] = res['name']
    obj['id'] = res['id']
    obj['duration_ms'] = res['duration_ms']
    obj['popularity'] = res['popularity']
    obj['explicit'] = res['explicit']
    obj['preview_url'] = res['preview_url']
    obj['spotify_uri'] = res['uri']
    return obj


# ------------
# get_playlist
# ------------

# spotify:user:1229502046:playlist:2GejolY4BJCsbUxf0yPydq
def get_playlist(user):
    global ACCESS_TOKEN
    if ACCESS_TOKEN is None:
        auth()
    ret = {}
    pl_info = (next(pl for pl in PLAYLISTS if pl['user'] == user), None)[0]
    print(pl_info)
    if pl_info is not None:
        url = 'https://api.spotify.com/v1/users/' + pl_info['user_id'] + '/playlists/' + pl_info['playlist_id']
        header = {'Authorization': 'Bearer {0}'.format(ACCESS_TOKEN), 'Content-Type': 'application/json'}
        res = requests.get(url, headers=header)
        res_obj = res.json()
        ret['followers'] = res_obj['followers']
        ret['description'] = res_obj['description']
        ret['images'] = res_obj['images']
        ret['owner'] = res_obj['owner']
        ret['tracks'] = res_obj['tracks']
    return ret
