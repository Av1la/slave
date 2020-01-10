"""
    
    ThreadBase é uma classe descendente de threading.Thread, possibilita 
    processamento em segundo plano, ou seja multiprocessamento quando alocado
    mais de um. 

    ThreadBase tem como diferencial a possibilidade de ser finalizado manual-
    mente via alguma interacao do usuario final.

    Diego @ 14/06/2019
"""

import threading
import inspect
import ctypes

from slave.app.utility import debug


class ThreadBase(threading.Thread):

    TERMINATED_NATURAL = 0  # finalizado naturalmente.
    TERMINATED_MANUAL = 1   # finalizado manualmente (self.terminate())


    def __init__(self):
        threading.Thread.__init__(self)
        self.terminated_status = ThreadBase.TERMINATED_NATURAL


    def terminate(self):

        if self.is_alive():

            ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self._ident),
                ctypes.py_object(SystemExit))

            if ret == 0:
                raise ValueError("invalid thread ident")
            if ret > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self._ident, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

            self.terminated_status = ThreadBase.TERMINATED_MANUAL

            debug('ThreadBase', '{thread} ({ident}) finished.'.format(
                thread=self.getName(), 
                ident=self._ident))
