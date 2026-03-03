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
pip install -r requirements.txt
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

## Chat

Com a ingestão concluída, inicie o chat interativo:

```
python src/chat.py
```

Digite sua pergunta e pressione Enter. Para encerrar, digite `sair`.

## Provedores de LLM

O projeto suporta dois provedores de LLM, configurados pela variável `LLM_PROVIDER` no `.env`:

| Provedor | Valor em `LLM_PROVIDER` | Variáveis necessárias |
|----------|-------------------------|-----------------------|
| OpenAI   | `openai`                | `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL` |
| Google   | `google`                | `GOOGLE_API_KEY`, `GOOGLE_MODEL`, `GOOGLE_EMBEDDING_MODEL` |

> **Importante:** `ingest.py` e `search.py` **devem usar o mesmo provedor**. O modelo de embeddings utilizado na ingestão precisa ser o mesmo da busca, pois os vetores armazenados no banco são gerados por ele.

> **Atenção ao trocar de provedor:** Se você alterar o `LLM_PROVIDER`, é necessário **apagar os dados do banco e reingerir o PDF**, pois os embeddings existentes foram gerados com o provedor anterior e são incompatíveis com o novo. Para isso, derrube o container e suba novamente:
> ```
> docker compose down -v
> docker compose up -d
> python src/ingest.py
> ```
