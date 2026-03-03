import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from ingest import get_embeddings, veficacao_variaveis
load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(questao = None):
  embeddings = get_embeddings()

  vetores = PGVector(
      embeddings=embeddings,
      collection_name=os.getenv("PGVECTOR_COLLECTION"),
      connection=os.getenv("PGVECTOR_URL"),
      use_jsonb=True,
  )

  chunks_resultados = vetores.similarity_search_with_score(questao, k=10)

  # Concatena o conteúdo de cada chunk para montar o contexto que será enviado à LLM.
  contexto = ""
  for doc, score in chunks_resultados:
    contexto += doc.page_content.strip()
    contexto += "\n\n"

  # Monta o template e a chain conforme o provedor definido em LLM_PROVIDER.
  llm = os.getenv("LLM_PROVIDER", "openai").lower()

  template = PromptTemplate(
    input_variables=["contexto", "pergunta"],
    template=PROMPT_TEMPLATE,
  )

  if llm == "google":
    from langchain_google_genai import ChatGoogleGenerativeAI

    modelo = ChatGoogleGenerativeAI(
      model = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash-lite"),
      temperature = 0,
      google_api_key = os.getenv("GOOGLE_API_KEY"),
    )
  else:
    from langchain_openai import ChatOpenAI

    modelo = ChatOpenAI(
      model = os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
      temperature = 0,
      api_key = os.getenv("OPENAI_API_KEY"),
    )

  # Criação da chain combinando o template e o modelo, e execução da chain com o contexto e a pergunta do usuário. 
  chain = template | modelo
  resposta = chain.invoke({"contexto": contexto, "pergunta": questao})

  print(resposta.content)

if __name__ == "__main__":
  search_prompt("Qual o faturamento da Empresa SuperTechIABrazil?")