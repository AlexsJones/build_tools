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


class options():
    command = "print_stats"
    gitlab_server = "http://gitlab.intranet.sky"
    gitlab_token = "QR18DoufKscQAF6HA_BD"
    gitlab_project = "ce-devices-ios/Benji"
    gitlab_max_size = 10

gs = gitlab_service()

merge, user_info = gs.run(options)

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, static_folder='public', template_folder=tmpl_dir)


@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/homepage")
def homepage():
    return render_template('homepage.html')

@app.route("/merge_requests")
def mrege_requests():
    return render_template('merge_requests.html', user_info=user_info)


if __name__ == "__main__":
  app.run(debug=True,port=2001)