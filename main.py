
from flask import Flask, render_template
app = Flask(__name__)


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
def tracks():
    return render_template('about.html')

if __name__ == "__main__":
    app.run()
