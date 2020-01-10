
import time
from app.queue import Queue

def mercado_pago():

    from app.workers.mercadopago import MercadoPagoSerializer

    serialized = MercadoPagoSerializer('db.txt', '|')
    queue = Queue(serialized.workers(), 100)
    queue.run()


def random_sleep():

    import os
    from app.workers.randomsleep import RandomSleepSerializer

    serialized = RandomSleepSerializer(50)
    queue = Queue(serialized.workers(), 10)
    queue.start()

    while not queue.finished:

        os.system('clear')
        workers = queue.get_active_workers()
        print('processos simultaneos:', len(workers))
        print('processos finalizados:', queue.finished_count)
        print('processos restantes:', len(queue.workers) - queue.finished_count)
        print('completo:', queue.get_percentual(), '%')
        print('\n')
        
        print('processos:')
        for worker in workers:
            print('{} {} sleep {}'.format(worker.__class__.__name__, worker.getName(), worker.sleep_time))

        print('\n\n')
        time.sleep(0.5)

random_sleep()