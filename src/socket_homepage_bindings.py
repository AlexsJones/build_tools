from flask_socketio import Namespace, emit
from flask import session, request, render_template
from build_tools.services.gitlab_service import gitlab_service
from threading import Thread
from src.options import options
from src.utils import get_first_day
thread = None
socket_global_ref = None


class HomePageSocketNameSpace(Namespace):

    def __init__(self, service, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.gs = service
        self.is_fetching=False

    @staticmethod
    def set_socket(s):
        global socket_global_ref
        socket_global_ref = s

    def thread_worker(self):
        merge, user_info = self.gs.run(options)

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

        fd = get_first_day()
        fd = fd.strftime("%d/%m/%Y")
        fd = "Totals from the last sprint which started on " + fd

        emit('populate_updates',
             {'total_open': to, 'total_closed': tc, 'total_wip': tw, "start_date": fd})

    @staticmethod
    def fill_table(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1

    @staticmethod
    def on_disconnect():
        print('Client disconnected', request.sid)