#! /usr/bin/env python
##########################################################################
#     File Name           :     app.py
#     Created By          :     jonesax
#     Creation Date       :     [2017-01-12 11:49]
#     Last Modified       :     [2017-01-12 14:33]
#     Description         :
##########################################################################

from flask import Flask, Response,render_template, request
import os
from build_tools.services.gitlab_service import gitlab_service
from datetime import datetime, timedelta

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, static_folder='public', template_folder=tmpl_dir)

def class_helper():
    class options():
        command = "print_stats"
        gitlab_server = "http://gitlab.intranet.sky"
        gitlab_token = "QR18DoufKscQAF6HA_BD"
        gitlab_project = "ce-devices-ios/Benji"
        gitlab_max_size = 10
        gitlab_stats_start_date = (datetime.now()-timedelta(days=14)).strftime("%d/%m/%Y")
        gitlab_stats_end_date = datetime.now().strftime("%d/%m/%Y")
    return options

@app.route("/")
def index():

    options = class_helper()

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

@app.route("/merge_requests")
def mrege_requests():
    options = class_helper()
    gs = gitlab_service()

    merge, user_info = gs.run(options)
    page_status = "Currently Showing requests from the last 2 weeks."
    return render_template('merge_requests.html', user_info=user_info, page_status=page_status)


def parse_string(d):
    s = d.split('-')
    f = "%s/%s/%s" % (s[2], s[1], s[0])
    return f

@app.route("/merge_requests", methods=["POST"])
def poster():
    options = class_helper()
    gs = gitlab_service()
    start_date = parse_string(request.form['start_date'])
    end_date = parse_string(request.form['end_date'])
    options.gitlab_stats_start_date = start_date
    options.gitlab_stats_end_date = end_date
    merge, user_info = gs.run(options)

    start_date = datetime.strptime(start_date, '%d/%m/%Y')
    if start_date > datetime.now():
        error_type = "The Start date cannot be in the future."
        return render_template('error.html', error_message=error_type)

    end_date = datetime.strptime(end_date, '%d/%m/%Y')
    if end_date > datetime.now():
        error_type = "The end date cannot be in the future."
        return render_template('error.html', error_message=error_type)
    if start_date > end_date :
        error_type = "The end date cannot be before the start date."
        return render_template('error.html', error_message=error_type)

    filtered_merges = []

    for x in merge:
        merge_date = gs.parse_datetime(x.created_at)
        if start_date <= merge_date <= end_date:
            filtered_merges.append(x)
    start_date = start_date.strftime('%d/%m/%Y')
    end_date = end_date.strftime('%d/%m/%Y')
    date_range = "Currently showing requests between " + start_date + " and " + end_date

    return render_template('merge_requests.html', user_info=user_info, page_status=date_range)

if __name__ == "__main__":
  app.run(debug=True,port=2001)