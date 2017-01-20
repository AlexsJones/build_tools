#! /usr/bin/env python
##########################################################################
#     File Name           :     app.py
#     Created By          :     jonesax
#     Creation Date       :     [2017-01-12 11:49]
#     Last Modified       :     [2017-01-12 14:33]
#     Description         :
##########################################################################

from flask import Flask, Response,render_template
import os
from build_tools.services.gitlab_service import gitlab_service
from datetime import datetime, timedelta

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, static_folder='public', template_folder=tmpl_dir)



@app.route("/")
def index():

    class options():
        command = "print_stats"
        gitlab_server = "http://gitlab.intranet.sky"
        gitlab_token = "QR18DoufKscQAF6HA_BD"
        gitlab_project = "ce-devices-ios/Benji"
        gitlab_max_size = 10
        gitlab_stats_start_date = (datetime.now()-timedelta(days=14)).strftime("%d/%m/%Y")
        gitlab_stats_end_date = datetime.now().strftime("%d/%m/%Y")

    gs = gitlab_service()

    merge, user_info = gs.run(options)

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
    return render_template('homepage.html', total_open=to, total_closed=tc, total_wip=tw)

# @app.route("/homepage")
# def homepage():
#     return render_template('homepage.html', total_open=to, total_closed=tc, total_wip=tw)
#
# @app.route("/merge_requests")
# def mrege_requests():
#     return render_template('merge_requests.html', user_info=user_info)
#
# @app.route("/", method=["POST"])
# def poster():
#     index();
#     #url for


if __name__ == "__main__":
  app.run(debug=True,port=2001)