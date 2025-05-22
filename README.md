# Projeto de Dockerização para a disciplina de DevOps
## Serviços:
- Banco de Dados: MongoDB.
- API: Python com FastAPI e Uvicorn.
- Frontend: Angular com nginx.

## Arquitetura:
Primeiramente, o banco de dados é inicializado, depois a API e por fim o frontend.  
O frontend faz requisições para a API e a API pega os dados do mongodb.  
A API então repassa os dados para o frontend.  

## Como rodar
$ git clone https://github.com/oznerot/docker_study.git
$ cd docker_study
$ docker compose up --build
