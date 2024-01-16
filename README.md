# Nomades-VH
Esse é um projeto para a equipe de Taekwondo "Nômades do Vale Histórico".

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

### 2. Criar um arquivo .env seguindo o exemplo do arquivo .env.example
```
cp .env.example .env
```
Depois disso, basta alterar as variáveis de ambiente.

### 3. Executar o container com postgres e pgbouncer
```
docker compose up pgbouncer
```

### 4. Poetry
 
``` 
poetry shell && poetry install
```

### 5. Executar projeto
```
python main.py
```
