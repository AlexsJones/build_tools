from flask_socketio import Namespace, emit
from flask import session, request, render_template
from build_tools.services.gitlab_service import gitlab_service
from datetime import datetime
from src.options import options
from src.utils import parse_string

thread = None
socket_global_ref = None


class MergeRequestSocketNameSpace(Namespace):
    def __init__(self, service, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.gs = service
        self.is_fetching = False

    @staticmethod
    def set_socket(s):
        global socket_global_ref
        socket_global_ref = s

    def on_requesting_updates(self, message):
        start_date = parse_string(message['start_date'])
        end_date = parse_string(message['end_date'])
        print(start_date, end_date)
        options.gitlab_stats_start_date = start_date
        options.gitlab_stats_end_date = end_date
        error = None
        merge, user_info = self.gs.run(options)

        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        if start_date > datetime.now():
            error = "The Start date cannot be in the future."

        end_date = datetime.strptime(end_date, '%d/%m/%Y')

        if start_date > end_date:
            error = "The end date cannot be before the start date."

        print(error)

        # filtered_merges = []
        #
        # for x in merge:
        #     merge_date = self.gs.parse_datetime(x.created_at)
        #     if start_date <= merge_date <= end_date:
        #         filtered_merges.append(x)
        # start_date = start_date.strftime('%d/%m/%Y')
        # end_date = end_date.strftime('%d/%m/%Y')
        #
        # if len(filtered_merges) == 0 and error is None:
        #     page_status = "No requests were made between " + start_date + " and " + end_date
        #     emit('filter_requests', {'page_status': page_status})
        # elif error is not None:
        #     page_status = ""
        #     emit('filter_requests', {'page_status': page_status})
        # else:
        #     page_status = "Currently showing requests between " + start_date + " and " + end_date
        #     emit('filter_requests', {'page_status': page_status})
        #
        #
        #
        # @staticmethod
        # def fill_table(self, message):
        #     session['receive_count'] = session.get('receive_count', 0) + 1
        #
        #
        #
        #     # start_date = parse_string(request.form['start_date'])
        #     # end_date = parse_string(request.form['end_date'])
        #     # options.gitlab_stats_start_date = start_date
        #     # options.gitlab_stats_end_date = end_date
        #     # error = None
        #     # merge, user_info = self.gs.run(options)
        #
        #
        #
        # @staticmethod
        # def on_disconnect():
        #     print('Client disconnected', request.sid)
