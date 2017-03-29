
from flask import Flask, render_template, request
import requests
app = Flask(__name__)


CLIENT_ID = "78237eb54be441c7bafdf02459e9d5ad"
CLIENT_SECRET = "3cde3d481c8b432ba6800e80412722a9"


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


@app.route("/spotifycallback", methods=['GET'])
def spotifycallback():
    code = request.args.get('code')
    state = request.args.get('state')
    error = requests.args.get('state')
    if error is not None:
        console.log("ERROR: " + error)
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



if __name__ == "__main__":
    app.run()
