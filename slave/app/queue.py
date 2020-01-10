

"""
    Descricao geral do modulo.

    Este modulo tem como objetivo criar filas de processamento utilizando
    threads. A fila no geral sera chamada de Queue, a queue possui um limite 
    maximo de processos simultaneos, quando o limite é ultrapassado é utilizada
    a fila. 

    QueueObserver
        -> Tem como objetivo iterar todos os processamentos em execucao, deter-
        mina a quantidade de processos e bloqueia a inicializacao de novos th-
        reads quando for necessario.

        QueueObserver é um thread da fila, o de index 0 (zero). Enquanto o 
        houver threads em atividade o mesmo se mantera em processamento. A sua
        inicializacao é automatica por meio da Queue.

"""

import time

from threading import Thread
from slave.app.thread import ThreadBase
from slave.app.utility import debug
from slave.app.utility import ProxySerializer


class QueueObserver(ThreadBase):

    def __init__(self, queue):
        ThreadBase.__init__(self)
        self.queue = queue


    def run(self):

        self.setName('QueueObserver')

        while True:

            tmp_finished_count = 0
            tmp_working_count = 0

            for worker in self.queue.workers:
                # worker iniciado
                if worker.is_started():
                    # worker em processamento
                    if worker.is_alive() and not worker.is_finished():

                        if (worker.started_at + self.queue.worker_timeout) <\
                                time.time():
                            self.queue.recycling.append(worker)
                            
                            worker.terminate()

                            worker.set_finished()
                            self.queue.finished_workers.append(worker)

                        else:
                            tmp_working_count += 1
                    else:
                        tmp_finished_count += 1
                        self.queue.finished_workers.append(worker)

            """ 
                pause fila, quando a quantidade maxima de processos
                simultaneos é atingida.
            """
            if tmp_working_count >= self.queue.maximum:
                self.queue.blocked = True
            else:
                self.queue.blocked = False

            """
                altera o queue count por ultimo para
                evitar erros de processamento. (ex. iniciar workers
                enquanto o processo de verificacao nao foi finalizado.)
            """
            self.queue.working_count = tmp_working_count
            self.queue.finished_count = tmp_finished_count

            # print('\rprocessos em andamento {threads}, finalizados {finisheds}'.format(
            #     threads=self.queue.working_count,
            #     finisheds=self.queue.finished_count), end='')

            """
                para o processamento quando a quantidade de processos 
                finalizados for exatamente igual a quantidade total
                de processos na queue.
            """
            if tmp_finished_count == len(self.queue.workers):
                self.queue.finished_at = time.time()

                print('finished. {:.2f}s'.format(
                    self.queue.finished_at - self.queue.started_at))
                self.queue.finished = True               
                break


class Queue(Thread):

    def __init__(self, workers, maximum=50, proxy_manager=None, worker_timeout=120):
        Thread.__init__(self)

        self.workers = workers
        self.finished_workers = []
        self.recycling = []

        self.maximum = maximum
        self.proxy_manager = proxy_manager
        self.worker_timeout = worker_timeout

        # pausar inicio de novos threads
        self.blocked = False
        
        self.working_count = 0  # processos rodando em simultaneo
        self.finished_count = 0 # processos finalizados
        self.observer = QueueObserver(self) # classe observer, gerencia a fila.

        self.started_at = None  # quando foi iniciado (timestamp)
        self.finished_at = None # quando foi finalizado.
        self.finished = False   # indica quando a fila foi finalizada.

        

        if proxy_manager and not type(proxy_manager) == ProxySerializer:
            raise TypeError('o proxy manager informado é invalido.')


    """
        quando o processamento for finalizado é possivel obter a duracao
        por meio deste metodo.
    """
    def get_processing_time(self):
        if self.finished:
            return (self.finished_at - self.started_at)
        return None


    """
        retorna uma lista de workers em atividade
    """
    def get_active_workers(self):

        active_workers = []

        if self.started_at is None or self.finished_at is not None:
            return active_workers

        for worker in self.workers:
            if not worker.is_started():
                continue

            if worker.is_finished():
                continue
            
            if not worker.is_alive():
                continue

            active_workers.append(worker)
        
        return active_workers


    def get_percentual(self):
        return round((self.finished_count / len(self.workers)) * 100, 2)


    def get_proxy_manager(self):
        return self.proxy_manager


    def run(self):

        self.started_at = time.time()

        # inicia o thread observer
        self.observer.start()

        for index, worker in enumerate(self.workers):

            while True:
                if self.blocked == True:
                    time.sleep(1)
                    continue

                break

            worker.setName('Worker #{index}'.format(
                index=index))

            worker.queue = self
            worker.start()
