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

#
# @app.route("/merge_requests")
# def merge_requests():
#     merge, user_info = gs.run(options)
#     print(options.gitlab_stats_start_date)
#     page_status = "Currently showing requests from the current sprint which started on " + options.gitlab_stats_start_date
#     return render_template('merge_requests.html', user_info=user_info, page_status=page_status)
#

def parse_string(d):
    s = d.split('-')
    f = "%s/%s/%s" % (s[2], s[1], s[0])
    return f

#
# @app.route("/merge_requests", methods=["POST"])
# def poster():
#     start_date = parse_string(request.form['start_date'])
#     end_date = parse_string(request.form['end_date'])
#     options.gitlab_stats_start_date = start_date
#     options.gitlab_stats_end_date = end_date
#     error = None
#     merge, user_info = gs.run(options)
#
#     start_date = datetime.strptime(start_date, '%d/%m/%Y')
#     if start_date > datetime.now():
#         error = "The Start date cannot be in the future."
#
#     end_date = datetime.strptime(end_date, '%d/%m/%Y')
#
#     if start_date > end_date:
#         error = "The end date cannot be before the start date."
#
#     filtered_merges = []
#
#     for x in merge:
#         merge_date = gs.parse_datetime(x.created_at)
#         if start_date <= merge_date <= end_date:
#             filtered_merges.append(x)
#     start_date = start_date.strftime('%d/%m/%Y')
#     end_date = end_date.strftime('%d/%m/%Y')
#
#     if len(filtered_merges) == 0 and error is None:
#         page_status = "No requests were made between " + start_date + " and " + end_date
#     elif error is not None:
#         page_status = ""
#     else:
#         page_status = "Currently showing requests between " + start_date + " and " + end_date
#
#     return render_template('merge_requests.html', user_info=user_info, error=error, page_status=page_status)
#

if __name__ == "__main__":

    gs = gitlab_service()

    home_name_space = HomePageSocketNameSpace(gs, '/home')
    home_name_space.set_socket(socketio)
    socketio.on_namespace(home_name_space)

    merge_name_space = MergeRequestSocketNameSpace(gs, '/merge_requests')
    merge_name_space.set_socket(socketio)
    socketio.on_namespace(merge_name_space)

    socketio.run(app, debug=True, port=2001)

