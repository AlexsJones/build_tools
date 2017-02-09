from flask_socketio import Namespace, emit
from flask import request
from flask import flash, redirect
from flask import current_app, url_for
from datetime import datetime
from src.options import options
import jsonpickle
thread = None
socket_global_ref = None
from src.temporary_storage_object import TemporaryStorageObject


class MergeRequestSocketNameSpace(Namespace):
    def __init__(self, service, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.gs = service
        self.results_store = dict([])

    @staticmethod
    def set_socket(s):
        global socket_global_ref
        socket_global_ref=s

    def fetch_updates(self, params):

        error = None
        start_date = params.gitlab_stats_start_date
        end_date = params.gitlab_stats_end_date

        key = start_date + "-" + end_date

        merge = None
        user_info = None
        if key in self.results_store.keys():
            # Use results that are stored
            storage_object = self.results_store.get(key)
            merge = storage_object.merge_data
            user_info = storage_object.user_data
        else:
            try:
                merge, user_info = self.gs.run(options)
            except Exception as s:
                print(str(s))
                emit('kill_loading', '{}')

            self.results_store[key] = TemporaryStorageObject(merge, user_info)

        if len(user_info) == 0 and error is None:
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

        start_date = message['start_date']
        end_date = message['end_date']

        if not start_date or not end_date:
            emit('kill_loading', '{}')
            emit('error', '{ error: "Date is required" ')
            return

        options.gitlab_stats_start_date = start_date
        options.gitlab_stats_end_date = end_date

        # Needs to be threaded out
        self.fetch_updates(options)

        @staticmethod
        def on_disconnect():
            print('Client disconnected', request.sid)