"""
    Worker base, deve ser utilizando para criar novos workers.
    Diego @ 15/06/2019
"""

import time
from slave.app.thread import ThreadBase


class WorkerBase(ThreadBase):

    def __init__(self, priority):
        ThreadBase.__init__(self)

        self.priority = 1
        
        self.started_at = None
        self.finished_at = None

        """
            a instancia de queue não deve ser 
            alterada por um worker. 
        """
        self.queue = None
        self.logs = []


    def is_started(self):
        if self.started_at:
            return True
        return False
    def is_finished(self):
        if self.finished_at:
            return True
        return False

    def set_started(self):
        self.started_at = time.time()
    def set_finished(self):
        self.finished_at = time.time()
        self.terminate()


    def set_log(self, ident, data):
        self.logs.append({
            'ident': ident,
            'data': data,
            'created_at': time.time()})
    def get_logs(self):
        return self.logs