from app.network.server import ServerProtocol


def create_server():
    server = ServerProtocol('127.0.0.1', 7777)
    server.start()
