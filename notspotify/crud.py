from notspotify import get_model
from flask import Blueprint, render_template, request
import spotify
import requests

API_VERSION = "v1"
ACCESS_TOKEN = None
CLIENT_ID = '78237eb54be441c7bafdf02459e9d5ad'
CLIENT_SECRET = '3cde3d481c8b432ba6800e80412722a9'
AUTH_HEADER = 'NzgyMzdlYjU0YmU0NDFjN2JhZmRmMDI0NTllOWQ1YWQ6M2NkZTNkNDgxYzhiNDMyYmE2ODAwZTgwNDEyNzIyYTk='
SCOPE = "playlist-read-private"

crud = Blueprint('crud', __name__)


@crud.route("/")
def base():
    return render_template('index.html')


@crud.route("/index.html")
def index():
    return render_template('index.html')


# [START list_artist]
@crud.route("/artists.html")
def artist():
    return render_template('artists.html')
# [END list_artist]


# [START list_albums]
@crud.route("/albums.html")
def albums():
    return render_template('albums.html')
# [END list_albums]


# [START list_tracks]
@crud.route("/tracks.html")
def tracks():
    return render_template('tracks.html')
# [END list_tracks]


@crud.route("/about.html")
def about():
    return render_template('about.html')


@crud.route("/login")
def login():
    # url = 'https://accounts.spotify.com/authorize?client_id=' + CLIENT_ID + '&response_type=code&redirect_uri=https%3A%2F%2Fnotspotify.me%2Fspotfiycallback&scope=' + SCOPE
    # res = requests.get(url)
    # res.raise_for_status()
    global ACCESS_TOKEN
    url = 'https://accounts.spotify.com/api/token'
    body = {
    	'grant_type': 'client_credentials'
    }
    headers = {'Authorization': 'Basic ' + AUTH_HEADER}
    print(headers)
    res = requests.post(url, data=body, auth=requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    ACCESS_TOKEN = res.json()['access_token']
    return ACCESS_TOKEN # TODO REMOVE


# ========================================================== #
# ---------------------- REST API -------------------------- #
# ========================================================== #

# ---------------------- ARTISTS ----------------------------#
@crud.route("/" + API_VERSION + "/artists", methods=['GET'])
def get_artists():
    if "id" in request.args:
        return spotify.get_artist_by_id(request.args.get('id'))
    elif "name" in request.args:
        return spotify.get_artist_by_name(request.args.get('name'))
    return spotify.get_artists()


# ------------------------ ALBUM ----------------------------#
@crud.route("/" + API_VERSION + "/album", methods=['GET'])
def get_albums():
    if "id" in request.args:
        return spotify.get_album_by_id(request.args.get('id'))
    elif "name" in request.args:
        return spotify.get_album_by_name(request.args.get('name'))
    return spotify.get_albums()


# ------------------------ TRACK ----------------------------#
@crud.route("/" + API_VERSION + "/track", methods=['GET'])
def get_tracks():
    if "id" in request.args:
        return spotify.get_track_by_id(request.args.get('id'))
    elif "name" in request.args:
        return spotify.get_track_by_name(request.args.get('name'))
    return spotify.get_tracks()


@crud.route("/spotifycallback", methods=['GET'])
def spotifycallback():
    code = request.args.get('code')
    state = request.args.get('state')
    error = requests.args.get('state')
    if error is not None:
        print("ERROR: " + error)
    else:
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https%3A%2F%2Fnotspotify.me%2Fspotfiycallback"
        }
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        res = requests.post('https://accounts.spotify.com/api/token', data=body, params=payload)

        # Create a user with the following creds
        access_token = res['access_token']
        token_type = res['token_type']
        scope = res['scope']
        expires_in = res['expires_in']
        refresh_token = res['refresh_token']
        # Stoped at step 6 https://developer.spotify.com/web-api/authorization-guide/
    return render_template('index.html')
