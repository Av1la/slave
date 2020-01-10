from time import sleep
from random import randint

from slave.app.workers.worker import Worker


class RandomSleepWorker(Worker):
    def __init__(self, priority=1):
        Worker.__init__(self, priority)
        self.sleep_time = randint(5, 10)

    def run(self):
        # self.started = True

        self.set_started()

        sleep(self.sleep_time)

        self.set_finished()
        # self.finished = True


class RandomSleepSerializer:
    def __init__(self, length):    
        self._workers = []
        for _ in range(length):
            self._workers.append(RandomSleepWorker())

    def workers(self):
        return self._workers
