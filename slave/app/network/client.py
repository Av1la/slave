import socket
from slave.app.thread import ThreadBase


"""
    Processo de Cliente.

    Utilizado pela Queue para criar uma conexao com a QueueMaster (Gestora
    de queues.).

    ** nao implementado.
"""
class ClientProtocol(ThreadBase):

    def __init__(self, host, port):
        ThreadBase.__init__(self)

        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        
        self.socket.connect((self.host, self.port))
        #self.socket.send
