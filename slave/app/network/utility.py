import json



RESPONSE_STATUS_CODE = {
    # 200 .. 299 - sucesso
    # 300 .. 399 - aviso 
    # 400 .. 499 - erro

    '200': 'OK',                    # requisicao aceita e processada.
    '400': 'BAD_REQUEST',           # request no formato incorreto.
    '401': 'INTERNAL_ERROR'         # exceptions
}


def NetworkRequest(header, body):
    return json.dumps({
        'header': header,    # autenticacao.
        'body': body,        # comandos para execucao.
    }).encode()


def ReadNetworkResponse(data):
    return json.loads(data)


def NetworkResponse(err, msg, res):
    return json.dumps({
        'err': err,  # bool erro.
        'msg': msg,  # string mensagem.
        'res': res   # object resposta do processo.
    }).encode()
