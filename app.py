
from flask import Flask, render_template, request
import spotify

app = Flask(__name__)

API_VERSION = "v1"


@app.route("/")
def base():
    return render_template('index.html')


@app.route("/index.html")
def index():
    return render_template('index.html')


@app.route("/artists.html")
def artist():
    return render_template('artists.html')


@app.route("/albums.html")
def albums():
    return render_template('albums.html')


@app.route("/tracks.html")
def tracks():
    return render_template('tracks.html')


@app.route("/about.html")
def about():
    return render_template('about.html')


@app.route("/login.html")
def login():
    return render_template('login.html')


# ========================================================== #
# ---------------------- REST API -------------------------- #
# ========================================================== #

# ---------------------- ARTISTS ----------------------------#
@app.route("/" + API_VERSION + "/artists" methods=['GET'])
def get_artists():
    if "id" in request.args:
        return spotify.get_artist_by_id(request.args.get('id'))
    elif "name" in request.args:
        return spotify.get_artist_by_name(request.args.get('name'))
    return spotify.get_artists()


# ------------------------ ALBUM ----------------------------#
@app.route("/" + API_VERSION + "/album" methods=['GET'])
def get_albums():
    if "id" in request.args:
        return spotify.get_album_by_id(request.args.get('id'))
    elif "name" in request.args:
        return spotify.get_album_by_name(request.args.get('name'))
    return spotify.get_albums()


# ------------------------ TRACK ----------------------------#
@app.route("/" + API_VERSION + "/track" methods=['GET'])
def get_tracks():
    if "id" in request.args:
        return spotify.get_track_by_id(request.args.get('id'))
    elif "name" in request.args:
        return spotify.get_track_by_name(request.args.get('name'))
    return spotify.get_tracks()


if __name__ == "__main__":
    app.run()
