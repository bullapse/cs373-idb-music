# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import subprocess
import os

from flask import current_app, Flask, url_for, render_template


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # Register the Bookshelf CRUD blueprint.
    from .crud import crud
    app.register_blueprint(crud)
    from .api import api
    app.register_blueprint(api)
    
    # Add a default root route.
    @app.route("/")
    def index():
        return render_template('index.html')

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    @app.route("/index.html")
    def index_main():
        return render_template('index.html')

    @app.route("/about.html")
    def about_page():
        return render_template('about.html')

    @app.route("/login")
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

    @app.route("/test")
    def test():

        script_dir = os.path.dirname('cs373-idb-music')
        rel_path = "tests.py"
        try:
            process = subprocess.check_output(["python", os.path.join(script_dir, rel_path)],
            stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            process = e.output

        return process.decode("utf-8")

    # @app.route("/spotifycallback", methods=['GET'])
    # def spotifycallback():
    #     code = requests.args.get('code')
    #     state = requests.args.get('state')
    #     error = requests.args.get('state')
    #     if error is not None:
    #         print("ERROR: " + error)
    #     else:
    #         body = {
    #             "grant_type": "authorization_code",
    #             "code": code,
    #             "redirect_uri": "https%3A%2F%2Fnotspotify.me%2Fspotfiycallback"
    #         }
    #         payload = {
    #             "client_id": CLIENT_ID,
    #             "client_secret": CLIENT_SECRET
    #         }
    #         res = requests.post('https://accounts.spotify.com/api/token', data=body, params=payload)
    #
    #         # Create a user with the following creds
    #         access_token = res['access_token']
    #         token_type = res['token_type']
    #         scope = res['scope']
    #         expires_in = res['expires_in']
    #         refresh_token = res['refresh_token']
    #         # Stoped at step 6 https://developer.spotify.com/web-api/authorization-guide/
    #     return render_template('index.html')

    return app


def get_model():
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'cloudsql':
        from . import model
        model = model
    # elif model_backend == 'datastore':
    #     from . import model_datastore
    #     model = model_datastore
    # elif model_backend == 'mongodb':
    #     from . import model_mongodb
    #     model = model_mongodb
    else:
        raise ValueError(
            "No appropriate databackend configured. "
            "Please specify datastore, cloudsql, or mongodb")

    return model
