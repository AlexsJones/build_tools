from flask_socketio import Namespace, emit
from flask import session, request
from threading import Thread
from src.options import options
thread = None
socket_global_ref = None
from src.temporary_storage_object import TemporaryStorageObject


class HomePageSocketNameSpace(Namespace):

    def __init__(self, service, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.gs = service
        self.results_store = dict([])

    @staticmethod
    def set_socket(s):
        global socket_global_ref
        socket_global_ref = s

    def thread_worker(self):

        key = options.gitlab_stats_end_date + "-" + options.gitlab_stats_end_date

        merge = None
        user_info = None
        if key in self.results_store.keys():
            # Use results that are stored
            storage_object = self.results_store.get(key)
            merge = storage_object.merge_data
            user_info = storage_object.user_data
        else:
            merge, user_info = self.gs.run(options)

            self.results_store[key] = TemporaryStorageObject(merge, user_info)

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
        emit('populate_updates',
             {'total_open': to, 'total_closed': tc, 'total_wip': tw})

    def on_requesting_updates(self, message):
        tr = Thread(target=self.thread_worker())
        tr.run()

    @staticmethod
    def fill_table(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1

    @staticmethod
    def on_disconnect():
        print('Client disconnected', request.sid)