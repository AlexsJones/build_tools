#! /usr/bin/env python
##########################################################################
#     File Name           :     app.py
#     Created By          :     jonesax
#     Creation Date       :     [2017-01-12 11:49]
#     Last Modified       :     [2017-01-12 14:33]
#     Description         :
##########################################################################

from flask import Flask, Response, render_template, request
from flask_socketio import SocketIO

from src.socket_homepage_bindings import HomePageSocketNameSpace
from src.socket_merge_request_bindings import MergeRequestSocketNameSpace
from build_tools.services.gitlab_service import gitlab_service
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, static_folder='bower_components', template_folder=tmpl_dir)
app.config['SECRET_KEY'] = 'test_key'
async_mode = 'threading'
socketio = SocketIO(app, async_mode=async_mode)


@app.route("/")
def index():

    return render_template("homepage.html")

@app.route("/merge_requests")
def merge_requests():
    return render_template("merge_requests.html")

if __name__ == "__main__":

    gs = gitlab_service()

    home_name_space = HomePageSocketNameSpace(gs, '/home')
    home_name_space.set_socket(socketio)
    socketio.on_namespace(home_name_space)

    merge_name_space = MergeRequestSocketNameSpace(gs, '/merge_requests')
    merge_name_space.set_socket(socketio)
    socketio.on_namespace(merge_name_space)

    socketio.run(app, debug=True, port=2001)

