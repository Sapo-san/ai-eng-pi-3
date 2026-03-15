import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)

from tracing.langfuse_config import langfuse_handler

# Modelo embeddings del .env
EMBEDDINS_MODEL = os.getenv('EMBEDDINGS_MODEL')

if not EMBEDDINS_MODEL:
    embeddings = OpenAIEmbeddings()
else:
    embeddings = OpenAIEmbeddings(model=EMBEDDINS_MODEL)




def load_documents(path, chunk_size=800, chunk_overlap=100):
    '''
    Carga un documento markdown y lo divide por headers y luego por caracteres

    '''

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Headers a considerar
    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
    ]

    # Split por headers
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )

    header_docs = markdown_splitter.split_text(text)

    # Segundo split para controlar tamaño máximo
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    final_docs = text_splitter.split_documents(header_docs)

    return final_docs

def create_vector_store(path, collection_name, chunk_size=800, chunk_overlap=100):
    '''
    Crea o carga un vector store persistente
    '''

    persist_dir = f"./rag/store/{collection_name}"

    # Si ya existe un vector store persistido → cargarlo
    if os.path.exists(persist_dir):
        print(f'Store preexistente detectado en: {persist_dir}')
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_dir
        )
        return vector_store

    # Si no existe → crearlo
    print(f'Creando store en: {persist_dir}')
    docs = load_documents(path, chunk_size, chunk_overlap)

    vector_store = Chroma.from_documents(
        docs,
        embeddings,
        collection_name=collection_name,
        persist_directory=persist_dir
    )

    return vector_store

# Crear los stores para cada agente
hr_vector = create_vector_store("data/hr_docs.md","hr_docs")
ti_vector = create_vector_store("data/ti_docs.md","ti_docs")
finance_vector = create_vector_store("data/finance_docs.md","finance_docs")

# Crear los retrievers
hr_retriever = hr_vector.as_retriever()
ti_retriever = ti_vector.as_retriever()
finance_retriever = finance_vector.as_retriever()