
import time
import os

from app.queue import Queue
from app.workers.mpmailcheck import MPMailFileSerializer
from app.utility import ProxySerializer

serialized = MPMailFileSerializer('res/db.txt', '|')
proxy_manager = ProxySerializer('res/proxyList.txt', ':')
queue = Queue(serialized.workers(), 100, proxy_manager=proxy_manager, worker_timeout=30)
queue.start()

started_at = time.time()
while not queue.finished:

    time.sleep(0.4)

    os.system('clear')

    print('em simultaneo: {} (maximo {}) {}%'.format(
        queue.working_count, queue.maximum, queue.get_percentual()))

    print('total: {}'.format(len(queue.workers)))
    print('processado: {}'.format(queue.finished_count))
    print('reciclagem: {}'.format(len(queue.recycling)))
    print('em espera: {}'.format(len(queue.workers) - queue.finished_count))
    print('\n')

    proxies_stats = queue.proxy_manager.get_stats()
    print('total de proxies: {}'.format(proxies_stats['total_counter']))
    print('proxies desabilitados: {}'.format(proxies_stats['disabled_counter']))
    print('total de erros: {}'.format(proxies_stats['error_counter']))

    print('\ntempo decorrido {:.02f}'.format(time.time() - started_at))

for worker in serialized.workers():
    print(worker.get_logs())


# response = input('deseja gerar uma db das contas verificadas? (sim/nao)')
# if response.lower() == 'sim':
#     for worker.

