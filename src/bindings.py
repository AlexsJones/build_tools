from flask_socketio import Namespace, emit


class Bindings(Namespace):
    def __init__(self, service, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.gs = service
        self.results_store = dict([])