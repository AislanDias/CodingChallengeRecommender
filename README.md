## Code Challenge: Movie Recommendation System
Using Python, Pandas, Numpy, Scikit-Learn and FastAPI
### Introdução

Realizei uma implementação própria do algoritmo de recomendação por filtragem colaborativa na sua variação usuário-usuário, baseado nas avaliaçoes dos usuários e ordenação das recomendações com base nas preferências pessoais do usuário. 

Buscando simular um caso de uso real, foi utilizado o dataset MovieLens 20M, obtendo como resultado de EQM (Erro Quadrático Médio) de 0.45 no conjunto de treinamento e de 0.59 no conjunto de testes, com 80% para treino e 20% para testes, considerando um subgrupo de 1000 usuários e 200 filmes dentro deste espectro.

### Como iniciar este projeto
```bash
# Baixar as imagens e contruir os containers
docker compose up
docker ps

# Abrir o shell do container criado
docker exec -it <build-id> bash

# Dentro do shell, executar os testes
# Povoamento das tabelas do banco de dados demora alguns minutos (~3min)
pytest -s -v
```

#### Documentation
localhost:8000/docs


### Portas utilizadas 

#### FastApi
3000 e 8000 

#### Postgres
5423
