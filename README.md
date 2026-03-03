# Desafio MBA Engenharia de Software com IA - Full Cycle

## Requisitos

*   Python 3.10+
*   Docker

## Instalação

Clone o repositório e entre na pasta do projeto. Em seguida, crie e ative um ambiente virtual:

```
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```
pip install -r requeriments.txt
```

Copie o arquivo de exemplo e preencha com suas credenciais:

```
cp .env.example .env
```

## Banco de dados

Suba o PostgreSQL com a extensão PGVector via Docker:

```
docker compose up -d
```

## Ingestão

Com o banco rodando e o `.env` configurado, execute:

```
python src/ingest.py
```
