

class InvalidRequestError(Exception):
    """ enviado um request fora do padrao esperado pelo protocolo. """
    pass


class InvalidResponseError(Exception):
    """ recebido uma resposta invalida, conforme o padrao esperado pelo 
    protocolo. """
    pass



