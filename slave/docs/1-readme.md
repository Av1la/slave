
Escrevendo workers.

- Worker

Para que uma queue consiga processar um dado é necessario um worker. O mesmo 
deve ser derivado de Worker (app.workers.worker). Para gerar diversos workers
apartir de uma lista de dados, é necessario montar um Serializer especifico 
para aquela informacao.

    metodos obrigatorios:

        run()       -> onde deve ser escrito o processo. (executado ao iniciar)
        terminate() -> finaliza um worker (derivado de Worker)


- Serializer 

O serializer é resposavel por instanciar um worker. O serializer busca as 
informacoes, estejam elas em um banco ou em um arquivo. As informacoes são 
agrupas e apartir disso o worker é instanciado. Obviamente cada worker devera
possuir o seu proprio serializer, levando em consideracao que cada worker pos-
suira um processamento diferente, assim dependendo de dados diferentes. Podem
existir workers para cada tipo de armazenamento de dado, Ex: arquivo, banco.

O conceito correto como é descrito na wiki seria o Deserializer, mas o projeto
foi montado utilizando a ideia de serialziers empregada no Django Framework.

https://en.wikipedia.org/wiki/Serialization

    metodos obrigatorios:

        workers() -> retorna uma lista de instancias do worker criado.

