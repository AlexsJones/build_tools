from flask_socketio import Namespace, emit
from flask import session, request, render_template
from datetime import datetime
from src.options import options
from src.utils import parse_string, toJson
import numpy as np
import json
import jsonpickle
thread = None
socket_global_ref = None
import json
import _thread


class MergeRequestSocketNameSpace(Namespace):
    def __init__(self, service, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.gs = service
        self.is_fetching = False

    @staticmethod
    def set_socket(s):
        global socket_global_ref
        socket_global_ref = s

    def threaded_fetch_updates_worker(self, params):


        error = None
        start_date = params.gitlab_stats_start_date
        end_date = params.gitlab_stats_start_date

        merge, user_info = self.gs.run(options)

        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        if start_date > datetime.now():
            error = "The Start date cannot be in the future."
            emit('error_raised',
                 {'error': error})

        end_date = datetime.strptime(end_date, '%d/%m/%Y')

        if start_date > end_date:
            error = "The end date cannot be before the start date."
            emit('error_raised',
                 {'error': error})

        filtered_merges = []

        for x in merge:
            merge_date = self.gs.parse_datetime(x.created_at)
            if start_date <= merge_date <= end_date:
                filtered_merges.append(x)
        start_date = start_date.strftime('%d/%m/%Y')
        end_date = end_date.strftime('%d/%m/%Y')

        if len(filtered_merges) == 0 and error is None:
            page_status = "No requests were made between " + start_date + " and " + end_date
            emit('page_status', {'page_status': page_status})
        elif error is not None:
            page_status = ""
            emit('page_status', {'page_status': page_status})
        else:
            page_status = "Currently showing requests between " + start_date + " and " + end_date
            emit('page_status', {'page_status': page_status})

        encoded_data = jsonpickle.encode(user_info)

        emit('table', encoded_data)

    def on_requesting_updates(self, message):

        start_date = parse_string(message['start_date'])
        end_date = parse_string(message['end_date'])
        options.gitlab_stats_start_date = start_date
        options.gitlab_stats_end_date = end_date

        # Needs to be threaded out
        self.threaded_fetch_updates_worker(options)

        @staticmethod
        def on_disconnect():
            print('Client disconnected', request.sid)