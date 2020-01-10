import sys
import time


from app.network.server import ServerProtocol 

def get_command_from_argv(command, argv):
    try:
        for arg in argv:
            if command in arg:
                return arg.split('=')[1:][0]
        return None
    except IndexError:
        print('falha ao interpretar argumento. ({})'.format(command))
        exit()


def main():

    cmd_type = get_command_from_argv('--type', sys.argv)
    if cmd_type == 'slave':

        cmd_worker = get_command_from_argv('--worker', sys.argv)
        if not cmd_worker:
            print('worker não definido. --worker=ClassWorker')
            exit()

        cmd_max = get_command_from_argv('--max', sys.argv)
        if not cmd_max:
            print('quantidade maxima de workers não informado. --max=integer')
            exit()

        cmd_server = get_command_from_argv('--server', sys.argv)
        if not cmd_server:
            print('servidor não especificado. --server=host:port')
            exit()

    elif cmd_type == 'server':

        cmd_host = get_command_from_argv('--host', sys.argv)
        if not cmd_host:
            print('hostname não definido. --host=127.0.0.1')
            exit()

        cmd_port = get_command_from_argv('--port', sys.argv)
        if not cmd_port:
            print('port não definido. --port=7777')
            exit()

        server = ServerProtocol(cmd_host, int(cmd_port))
        server.start()

        time.sleep(5)
        server.terminate()

    elif not cmd_type:
        print('o tipo de execucao deve ser informado. --type=server')
        exit()


main()

