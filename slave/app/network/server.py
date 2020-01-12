
import socket
from json.decoder import JSONDecodeError

from slave.app.thread import ThreadBase
from slave.app.network.utility import NetworkRequest
from slave.app.network.utility import NetworkResponse
from slave.app.network.utility import ReadNetworkResponse

from slave.app.network.exceptions import BadTerminateSocketThread



class ServerProtocol(ThreadBase):
    """
        Processo de Servidor.

        O processo abaixo cria um servidor para gerenciamento de queues.
        A partir do servidor é possivel criar/gerir/consultar queues.
    """

    def __init__(self, host, port):
        ThreadBase.__init__(self)

        self.running = True

        self.host = host
        self.port = port
        self.connections = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(0.5)
        self.socket.bind((self.host, self.port))


    def broadcast(self, networkrequest):
        for connection in self.connections:
            connection.send(networkrequest)


    def terminate(self):

        for connection in self.connections:
            connection.close('the server closed the connection')

        self.running = False
        self.socket.close()
        super().terminate()


    def run(self):

        self.setName('ServerProtocol')
        self.socket.listen()
        print('server listen on {}:{}'.format(self.host, self.port))

        while self.running:
            try:
                conn, addr = self.socket.accept()
                print('connection recieved from {}'.format(addr))

                connection = ServerConnectionProtocol(conn, addr)
                self.connections.append(connection)
                connection.start()
            except socket.timeout:
                pass



class ServerConnectionProtocol(ThreadBase):
    """
        ServerConnectionProtocol representa uma conexao ativa com o sistema.

        Gerencia uma conexão de um cliente com o servidor, nessa arquitetura é
        a interface entre o cliente e o servidor. É o meio de conexao do servidor
        como o cliente.
    """

    def __init__(self, socket, addr):
        ThreadBase.__init__(self)
        self.socket = socket
        self.socket.settimeout(1)
        self.addr = addr
        self.connected = False


    # envia uma mensagem ao cliente.
    def send(self, data):
        if self.connected:
            self.socket.send(data)


    # fecha a conexao de socket com o cliente.
    def close(self, msg):
        if self.connected:
            self.send(NetworkResponse(True, msg, []))
            self.connected = False
            self.socket.close()
            print('connection closed {}'.format(self.addr))
            super().terminate()


    # finaliza o thread.
    def terminate(self):
        raise BadTerminateSocketThread('please use the close() method.')


    def run(self):

        self.connected = True
        self.setName('ConnectionProtocol {}'.format(self.addr))

        while self.connected:
            try:
                recv_data = self.socket.recv(1024)
                serielized_data = ReadNetworkResponse(recv_data).decode()

                print('{}:{} > {}'.format(*(self.addr), serielized_data))
                self.send(NetworkResponse(False, 'OK', []))

            except JSONDecodeError:
                print('bad request from {}:{}'.format(*(self.addr)))
                self.close('BAD REQUEST')
                break

            except socket.timeout:
                pass
