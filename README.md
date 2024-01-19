# Nomades-VH
Esse é um projeto para a equipe de Taekwondo "Nômades do Vale Histórico".

## Requisitos
 - PYTHON >= 3.12
 - DOCKER, DOCKER-COMPOSE
 - POETRY


## Executar projeto

### 1. Baixar do repositório
#### SSH
```
git clone git@github.com:Nomades-VH/API-Nomades.git
```
#### HHTP

```
git clone https://github.com/Nomades-VH/API-Nomades.git
```

### 2. .ENV
### Criar um arquivo .env
```
cp .env.example .env
```
### Exportar as váriaveis do arquivo .env
```
export $(cat .env | xargs)
```

### 3. Poetry

``` 
poetry shell && poetry install
```

### 4. Executar o container com postgres e pgbouncer
#### PRODUÇÃO
```
make run-server
```

#### DESENVOLVIMENTO
```
make run-dev-server
```



