# Use this import to avoid cyclic imports with type checking (requires Python >= 3.7)
from __future__ import annotations

# Imports
import flask
from flask import request
from flask import json
from datetime import datetime

# Path to static HTML/JS/CSS files that are served for the WebUI
# also check in APIController.py when handler gets bound to address
static_html_folder = "webserver/pixida-web-ui/dist"


class WebServer:
    def __init__(self, controller: Controller, host: str = '0.0.0.0', port: int = 10000) -> None:
        # Init class members
        self._app = flask.Flask(__name__)
        self._controller = controller
        self._host = host
        self._port = port

        # Init routes
        @self._app.route('/', methods=['GET'])
        def index():
            # Serve main website (index.html)
            return flask.send_from_directory(static_html_folder, 'index.html')

        @self._app.route('/data', methods=['GET'])
        def data():
            # Data interface
            # datetime.fromtimestamp(ms/1000.0) # JS uses ms, unix is in s
            # start_time = request.args.get('start', default=None, type=None)

            start_time = datetime.fromtimestamp(float(request.args.get('start'))/1000.0)
            end_time = datetime.fromtimestamp(float(request.args.get('end'))/1000.0)
            lineid = request.args.get('line')
            busid = request.args.get('bus')
            station = request.args.get('station')

            response = self._app.response_class(
                response=json.dumps(self._controller.get_data(start_time, end_time, lineid, busid, station)),
                status=200,
                mimetype='application/json'
            )
            return response

        @self._app.route('/favicon.ico', methods=['GET'])
        def serve_favicon():
            # Serve favicon
            return flask.send_from_directory(static_html_folder, 'favicon.ico')

        @self._app.route('/<path:p>/<filename>', methods=['GET'])
        def serve_files(p, filename):
            # Serve additional files
            return flask.send_from_directory(static_html_folder+'/'+p, filename)

    def start_server(self) -> None:
        # Start server
        self._app.run(host=self._host, port=self._port)
        print('Start server on host ' + str(self._host) +
              ' on port ' + str(self._port))

    def stop_server(self) -> None:
        # Stop server
        print('Stop server on host ' + str(self._host) +
              ' on port ' + str(self._port))
