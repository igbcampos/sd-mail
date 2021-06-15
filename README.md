# Microsserviços

O projeto realizado trata-se de uma implementação de um serviço de mensagens, onde foi desenvolvido uma API e um cliente de e-mail. Implementados na linguagem Python, a API faz uso da micro framework Flask e o Cliente utiliza a biblioteca Django. A autenticação, armazenamento e manipulação é enviado pelo Cliente e feito na API, tal como essas informações são trocadas usando o formato JSON. 

Além disso, no desenvolvimento do servidor de email utilizou-se WebServices no modelo REST, onde foi implementado as seguintes funcionalidades: enviar, listar, apagar, abrir, encaminhar e responder mensagens.

## Execução

Para executar as aplicações faz-se necessário ter o Docker instalado. Para iniciar a execução basta clicar para executar o script **start.cmd** que se encontra na raíz do projeto.

## API

### Endpoints

Para testar a API, foi usado o [Postman](https://www.postman.com/downloads/), outros programas de requição http podem ser usados, respeitando os parâmetros requisitados em cada chamada. Os endpoints a seguir estão disponíveis, a descrição dos cabeçalhos e parâmetros necessários segue cada um deles:

* [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register)
Método: POST
Body: 
    raw; 
    JSON;
    {
        "name": "Jane",
        "email": "jane@mail.com",
        "password": "1234"
    }

* [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
Método: GET
Authorization: Type: Basic Auth; Username: **email**; Password: **senha**;

* [http://127.0.0.1:5000/me](http://127.0.0.1:5000/me)
Método: GET
Headers: x-access-tokens: **token**;

* [http://127.0.0.1:5000/emails](http://127.0.0.1:5000/emails)
Método: POST
Headers: x-access-tokens: **token**;
Body: 
    raw; 
    JSON; 
    {
        "receiver": "john@mail.com",
        "subject": "Teste",
        "body": "Teste"
    }

* [http://127.0.0.1:5000/emails/received](http://127.0.0.1:5000/emails/received)
Método: GET
Headers: x-access-tokens: **token**;

* [http://127.0.0.1:5000/emails/sent](http://127.0.0.1:5000/emails/sent)
Método: GET
Headers: x-access-tokens: **token**;

* [http://127.0.0.1:5000/emails/forward](http://127.0.0.1:5000/emails/forward)
Método: POST
Headers: x-access-tokens: **token**;
Body: 
    raw; 
    JSON; 
    {
        "receiver": "john@mail.com",
        "email_id": 1
    }

* [http://127.0.0.1:5000/emails/reply](http://127.0.0.1:5000/emails/reply)
Método: POST
Headers: x-access-tokens: **token**;
Body: 
    raw; 
    JSON; 
    {
        "email_id": 1,
        "body": "Teste"
    }

## Cliente

### Endpoints

No cliente é possível criar uma conta, fazer login, consultar os e-mails enviados e os recebidos, responder e encaminhar. O sistema já possui dois usuários: maria@maria.com e jane@mail.com, ambos com senha **1234**. O sistema só permite o envio de mensagens para usuários cadastrados.

Os endpoints a seguir estão disponíveis:

* [http://localhost:8000/login](http://localhost:8000/login)
* [http://localhost:8000/register](http://localhost:8000/register)
* [http://localhost:8000/](http://localhost:8000/)
* [http://localhost:8000/send-email](http://localhost:8000/send-email)
* [http://localhost:8000/sent](http://localhost:8000/sent)