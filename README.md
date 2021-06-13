# Microsserviços

Conforme solicitado pelo professor, foi desenvolvido uma API e um cliente de e-mail. Ambos foram feitos usando a linguagem python, sendo que a primeira faz uso da micro framework Flask, enquanto o sendo usa a biblioteca Django. Toda a autenticação e o armazenamento e manipulação é enviado pelo cliente e feito na api, e essas informações são trocadas usando o formato JSON. 

Para o propósito de entimento de como os microsserviços funcionam e como as requisições são tratadas internamente, foi pedido também, que fosse usado ferramentas de baixo nível. O Flask me pareceu uma boa escolha. Espero que, pelo amor de Deus, não haja problema.

## API

### Setup

Para a execução correta da API é necessário: criar o ambiente virtual, instalar o sqlite3, criar as tabelas no banco de dados e iniciar a execução do servidor. Os seguintes passos tratam de cada uma dessas etapas, respectivamente:

#### Criar ambiente Virtual

No terminal, no diretório api, digite os seguintes comandos:

```
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

#### Instalar sqlite3

1. Baixar o [sqlite3](https://sqlite.org/download.html), na opção Precompiled Binaries for Windows > sqlite-tools-win32-x86-3340000.zip

2. Criar a pasta **sqlite3** em **C:** e colar os arquivos extraídos do download feito no passo 1 (sqldiff, sqlite3 e sqlite3_analyzer).

2. Adicionar a pasta **C:\sqlite3** ao **path** do Windows.

#### Criar tabelas e iniciar servidor

No terminal, no diretório api, digite os seguintes comandos:

```
sqlite3 database.db
^C

python

from app import db
db.create_all()

exit()

set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

### Executando

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

[Acesse o cliente](https://sdmail.herokuapp.com)

### Setup

Para a execução correta do cliente é necessário: criar o ambiente virtual, criar as tabelas no banco de dados e iniciar a execução do servidor. Os seguintes passos tratam de cada uma dessas etapas, respectivamente:

#### Criar ambiente Virtual, criar tabelas e iniciar servidor

No terminal, no diretório client, digite os seguintes comandos:

```
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
set BASE_URL=http://127.0.0.1:5000
python manage.py runserver
```

### Executando

No cliente é possível criar uma conta, fazer login, consultar os e-mails enviados e os recebidos. É importante destacar só é possível enviar mensagens para usuários já cadastrados no sistema. O sistema já possui dois usuários: igbcampos@mail.com e john@mail.com, ambos com senha **1234**.

Os endpoints a seguir estão disponíveis:

* [http://localhost:8000/login](http://localhost:8000/login)
* [http://localhost:8000/register](http://localhost:8000/register)
* [http://localhost:8000/](http://localhost:8000/)
* [http://localhost:8000/send-email](http://localhost:8000/send-email)
* [http://localhost:8000/sent](http://localhost:8000/sent)