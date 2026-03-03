import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_postgres import PGVector
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

# Verifica as variáveis de ambiente necessárias para a execução do script.
def veficacao_variaveis():
    llm = os.getenv("LLM_PROVIDER", "openai").lower()
    variaveis_obrigatorias = ["PGVECTOR_URL", "PGVECTOR_COLLECTION", "PDF_PATH"]
    variaveis_obrigatorias += ["OPENAI_API_KEY"] if llm == "openai" else ["GOOGLE_API_KEY"]
    for k in variaveis_obrigatorias:
        if not os.getenv(k):
            raise RuntimeError(f"A variável ambiente {k} não está definida no .env")

# Retorna o modelo de embeddings conforme o provedor definido em LLM_PROVIDER.
def get_embeddings():
    llm = os.getenv("LLM_PROVIDER", "openai").lower()

    if llm == "google":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        model = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")
        
        return GoogleGenerativeAIEmbeddings(model=model)
    else:
        from langchain_openai import OpenAIEmbeddings
        model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        
        return OpenAIEmbeddings(model=model)

def ingest_pdf():
    pdf_caminho = os.getenv("PDF_PATH")

    # Obtém conteúdo do PDF "document.pdf"
    conteudo_pdf = PyPDFLoader(str(pdf_caminho)).load()

    #Obtém as configurações de tamanho de chunk e overlap
    tamanho_chunk = int(os.getenv("CHUNK_SIZE","1000"))
    overlap_chunk = int(os.getenv("CHUNK_OVERLAP","150"))

    # Quebra o conteúdo em chunks conforme tamanho e overlaps.
    chunks_pdf = RecursiveCharacterTextSplitter(
        chunk_size = tamanho_chunk, 
        chunk_overlap = overlap_chunk, add_start_index=False).split_documents(conteudo_pdf)
    if not chunks_pdf:
        raise SystemExit(0)

    # Realiza o enriquecimento dos chunks, removendo metadados vazios ou nulos.
    enriquecido = []
    for d in chunks_pdf:
        meta = {k: v for k, v in d.metadata.items() if v not in ("", None)}
        novo_documento = Document(
            page_content = d.page_content,
            metadata = meta
        )
        enriquecido.append(novo_documento)

    # Obtém o modelo de embeddings conforme o provedor definido em LLM_PROVIDER.
    embeddings = get_embeddings()

    # Realiza o armazenamento dos embeddings no PostgreSQL utilizando a extensão PGVector.
    gravacao_vetores = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )

    # Define os índices (ids) para cada documento a ser armazenado, utilizando o formato "documento-{i}".
    ids = [f"documento-{i}" for i in range(len(enriquecido))]

    gravacao_vetores.add_documents(documents=enriquecido, ids=ids)
    pass

if __name__ == "__main__":
    veficacao_variaveis()
    ingest_pdf()