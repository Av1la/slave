
import random
import uuid

DEBUG = True

def debug(level, message):
    if DEBUG:

        print('{level} -> {message}'.format(
            level=level,
            message=message))


class ProxySerializer():

    def __init__(self, path, separator, max_errors=10):
        self.path = path
        self.separator = separator
        self.max_errors = max_errors

        self.proxies = []
        self.intelligent_proxies = []

        self.get_proxies()

    def get_proxies(self):

        self.proxies = []

        with open(self.path, 'r') as opened_file:
            tmp_servers = []
            
            for line in opened_file.readlines():
                line = line.replace('\n', '')
                if len(line) and self.separator in line:
                    
                    tmp_server = '{}:{}'.format(*(line.split(self.separator)))
                    
                    if not tmp_server in tmp_servers:
                        proxies = {
                            'uuid': str(uuid.uuid4()),
                            'http': tmp_server,
                            'https': tmp_server,
                            'error_counter': 0,
                            'uses_counter': 0,
                            'pyrequests': {
                                'http': tmp_server,
                                'https': tmp_server,
                            }
                        }

                        tmp_servers.append(tmp_server)
                        self.proxies.append(proxies)

        return self.proxies


    def get_random(self):

        if len(self.proxies):
            index = random.randint(0, len(self.proxies) - 1)
            return self.proxies[index]

        return False


    """
        Retorna um proxy diferente dos ultimos proxies informados.
        A quantidade até que o proxy possa ser utilizado novamente é informado
        no parametro max_cache.

        Diego @ 23/06/2019
    """
    def get_intelligent_random(self, max_cache=10):

        # caso a lista de proxies seja menor que o maximo de cache permitido
        if not len(self.proxies) >= max_cache:
            return self.get_random()

        while True:
            proxies = self.get_random()
            
            if not proxies in self.intelligent_proxies:

                if proxies['error_counter'] >= self.max_errors:
                    continue

                proxies['uses_counter'] += 1
                self.intelligent_proxies.append(proxies)
                return proxies

        # quando a quantidade maxima de proxies no cache é ultrapassada
        # o registro mais antigo é removido da lista.
        if len(self.intelligent_proxies) >= max_cache:
            self.intelligent_proxies.pop(0)


    def set_failed(self, proxies):

        for index, proxy in enumerate(self.proxies):
            if proxy['uuid'] == proxies['uuid']:
                self.proxies[index]['error_counter'] += 1
                return True

        return False
    
    def get_stats(self):

        error_counter = 0
        disabled_counter = 0

        for proxies in self.proxies:
            error_counter += proxies['error_counter'] 

            if proxies['error_counter'] >= self.max_errors:
                disabled_counter += 1

        return {
            'total_counter': len(self.proxies),
            'error_counter': error_counter,
            'disabled_counter': disabled_counter
        }