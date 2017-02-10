#! /usr/bin/env python
##########################################################################
#     File Name           :     app.py
#     Created By          :     jonesax
#     Creation Date       :     [2017-01-12 11:49]
#     Last Modified       :     [2017-01-12 14:33]
#     Description         :
##########################################################################

import os
import random
import string
import threading
from src.options import options
import jsonpickle
from src.temporary_storage_object import TemporaryStorageObject
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, close_room, leave_room, rooms
from build_tools.services.gitlab_service import gitlab_service

# Configuration #################################################################################
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, static_folder='bower_components', template_folder=tmpl_dir)
app.config['SECRET_KEY'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
async_mode = 'threading'
socketio = SocketIO(app, async_mode=async_mode)
results_store = dict([])
gs = gitlab_service()
# Routes #######################################################################################


@app.route("/")
def index():

    return render_template("homepage.html")


@app.route("/merge_requests")
def merge_requests():
    return render_template("merge_requests.html")
# Socketio #####################################################################################

default_room = 'ce-devops-stats-room'


@socketio.on('connect', namespace='/bindings')
def connect():

    join_room(default_room)
    print('Client ' + request.sid + " joined room " + default_room)
    print(rooms())


@socketio.on('disconnect', namespace='/bindings')
def disconnect():
    leave_room(default_room)
    print('Client ' + request.sid + " left room " + default_room)


# Logic ########################################################################################
@socketio.on('fetch_merge_request_updates', namespace='/bindings')
def fetch_merge_request_updates(params):
    error = None

    start_date = params.get('start_date')
    end_date = params.get('end_date')

    key = start_date + "-" + end_date

    o = options()
    o.gitlab_stats_start_date = start_date
    o.gitlab_stats_end_date = end_date

    merge = None
    user_info = None
    if key in results_store.keys():
        # Use results that are stored
        storage_object = results_store.get(key)
        merge = storage_object.merge_data
        user_info = storage_object.user_data
    else:
        try:
            merge, user_info = gs.run(options)
        except Exception as s:
            print(str(s))
            emit('kill_loading', '{}')

        results_store[key] = TemporaryStorageObject(merge, user_info)

    if len(user_info) == 0 and error is None:
        page_status = "No requests were made between " + start_date + " and " + end_date
        socketio.emit('page_status', {'page_status': page_status})
    elif error is not None:
        page_status = ""
        socketio.emit('page_status', {'page_status': page_status})
    else:
        page_status = "Currently showing requests between " + start_date + " and " + end_date
        socketio.emit('page_status', {'page_status': page_status})

    encoded_data = jsonpickle.encode(user_info)

    socketio.emit('table', encoded_data, namespace='/bindings')


def poll_homepage_updates():
    print("Fetching....")

    key = options.gitlab_stats_end_date + "-" + options.gitlab_stats_end_date

    merge = None
    user_info = None
    if key in results_store.keys():
        # Use results that are stored
        storage_object = results_store.get(key)
        merge = storage_object.merge_data
        user_info = storage_object.user_data
    else:
        merge, user_info = gs.run(options)

        results_store[key] = TemporaryStorageObject(merge, user_info)

    to = 0
    tc = 0
    tw = 0

    for x in merge:
        print(x.title)

        if "WIP" in x.title:
            tw += 1
        if x.state == 'opened':
            to += 1
        if x.state == 'closed':
            tc += 1

    to = to - tw

    socketio.emit('homepage_room_updates',
         {'total_open': to, 'total_closed': tc, 'total_wip': tw}, room=default_room, namespace='/bindings')

    threading.Timer(5, poll_homepage_updates).start()
################################################################################################
if __name__ == "__main__":

    poll_homepage_updates()

    socketio.run(app, debug=False, use_reloader=False)
