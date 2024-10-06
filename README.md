# API para detecção de placas carros

Essa API RESTful de detecão de placas de carros foi desenvolvida primeiramente para o meu trabalho de conclusão de curso em **Sistemas de Informações**. 

O projeto foi resgatado e foi realizido algumas atualizações, criando novas funcionadlidades, melhorando a organização dos arquivos, realizando a refatoração do código utilizando boas práticas e mantendo as convenções da linguagem Python.


## 🚀 Tecnologias utilizadas
<div align="left">
    <a href="https://skillicons.dev">
        <img src="https://skillicons.dev/icons?i=python,opencv,flask,mysql,postman"/>
    </a>
</div>

## 🖥️ API RESTful

### Arquitetura:
```
meu_repositorio/
├── main.py                        # Inicia a aplicação.
requirements.txt                   # Contém todas as dependências necessárias para executar o projeto.
.gitignore                         # Arquivo para o git ignorar arquivos e pastas desnecessárias.
.env                               # Armazena as variáveis de ambiente.
README.md
 views/
|   ├── carro.py                   # Rotas referentes aos carros.
|   ├── services.py                # Rotas referentes aos serviços.
|   ├── usuario.py                 # Rotas referentes aos usuários e autenticação.
├── settings/
|   ├── config.py                  # Configurações que recebem as variáveis de ambiente.
├── services/
|   ├── email.py                   # Serviço responsável por enviar e-mail de recuperação de conta.
|   ├── imagem_ocr.py              # Serviço responsável por realizar o OCR da imagem da placa do carro.
├── scripts/
|   ├── preparar_banco.py          # Script para configurar o banco de dados localmente.
├── models/
|   ├── carro.py                   # Model representando a tabela carro.
|   ├── usuario.py                 # Model representando a tabela usuario.
├── content/                       # Diretório que armazena um backup das imagens enviadas pela rota de upload de arquivos
|   ├── img1.png                   
|   ├── img2.png
|   ├── img3.png ...
|   ├── logo/                      # Diretório que armazena a imagem do logo que é enviado como assinatura no e-mail
|   |   ├── guarda.png
```

### Documentação:

O arquivo **ROTAS.md** contém informações sobre os endpoints da API: [Readme das rotas da API]()

## 🛠️ Como executar?
Para executar esse projeto é necessário seguir o passo a passo a seguir:

1. Criar o ambiente virtual do Python.

Na pasta raíz do repositório local, execute o comando:
```
python -m venv <nome do ambiente virtual>
```

2. Ativar o ambiente virutal
```
.\venv\Scripts\activate
```

3. Instalar as dependências do **requirements.txt**.
```
pip install -r requirements.txt
```

4. Executar o arquivo **prepara_banco.py** para criação do banco de dados e tabelas.
```
python prepara_banco.py
```

5. Criar o arquivo **.env** com os dados as variáveis de ambiente.
```
JWT_SECRET_KEY=senha
SQLALCHEMY_DATABASE_URI=uri_banco
SMTP_SERVER=servidor_smtp
SMTP_PORT=porta
SMTP_EMAIL=email_smtp
SMTP_SENHA=senha_smtp
CONTENT_FOLDER=content
```

6. Executar o arquivo **main.py** que deseja através do comando:
```
python main.py
```

## 📝 Testes

Para testar essa API, você poderá utilizar a ferramenta Postman.

Esse link contém um totorial de como usar a ferramenta: [Tutorial Postman](https://gist.github.com/zec4o/f4a600fafa50003e315fa3fcfd9c1e4a)

## 📁 Documentações de referência
[Documentação OpenCV](https://opencv.org/)
<br>
[Documentação Tesseract](https://tesseract-ocr.github.io/)
<br>
[Documentação EasyOCR](https://jaided.ai/easyocr/)
<br>
[Documentação Flask](https://flask.palletsprojects.com/en/3.0.x/)
<br>

***
# 🖥️ Rotas da API

## Index
```
GET /
```
Rota principal que redireciona para a rota de autenticação.

## Autenticar
```
POST /autenticar
```
Permite que os usuários se autentiquem usando suas credenciais (email e senha).

**Parâmetros:**
```
{
    "email": "string",
    "senha": "string"
}
```

## Cadastrar Usuário
```
POST /cadastrar-usuario
```
Rota que permite cadastrar um novo usuário.

**Parâmetros:**
```
  {
      "email": "string",
      "nome": "string",
      "sobrenome": "string",
      "senha": "string"
  }
```

## Editar Usuário
```
PUT /editar-usuario/<string:email>
```
Permite que o usuário edite suas informações pessoais pelo email.

**Parâmetros:**
```
  {
      "nome": "string",
      "sobrenome": "string",
      "senha": "string"
  }
```

## Deletar Usuário
```
DELETE /deletar-usuario/<string:email>
```
Permite que o usuário delete sua conta pelo email.

## Resetar Senha
```
POST /email
```
Rota para resetar senha via e-mail.

**Parâmetros:**
```
  {
      "email": "string"
  }
```

## Upload Arquivo
```
POST /upload-arquivo
```
Permite que o usuário realize o upload de uma imagem e retorna a placa detectada.

**Parâmetros:**
```
HEADERS
Key: Content-Type
Value: multipart/form-data

BODY
Key: nome_do_arquivo
Value: arquivo.png
```

## Consultar Carros
```
GET /carros
```
Consulta todos os carros cadastrados.

## Consultar Carro Específico
```
GET /carros/<int:id>
```
Consulta um carro específico pelo seu ID.

## Cadastrar Carro
```
POST /cadastrar-carro
```
Cadastra um novo carro.

**Parâmetros:**
```
{
    "colaborador": "string",
    "modelo": "string",
    "numero_placa": "string"
}
```

## Editar Carro
```
PUT /editar-carro/<int:id>
```
Altera um carro já cadastrado através do seu ID.

**Parâmetros:**
```
{
    "colaborador": "string",
    "modelo": "string"
}
```

## Deletar Carro
```
DELETE /deletar-carro/<int:id>
```
Deleta um carro pelo seu ID.

## Verificar Status do veículo
```
POST /status/<string:numero_placa>
```
Verifica o status do veículo pela placa.

***
