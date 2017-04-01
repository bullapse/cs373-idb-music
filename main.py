
import notspotify
import config
# import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
# requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)
app = notspotify.create_app(config)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
