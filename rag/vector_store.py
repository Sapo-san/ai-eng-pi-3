from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from tracing.langfuse_config import langfuse_handler

embeddings = OpenAIEmbeddings()

def load_documents(path):
    '''
    Carga un documento
    '''
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return [Document(page_content=text)]

def create_vector_store(path, collection_name):
    '''
    Crea un vector store
    '''
    docs = load_documents(path)

    vector_store = Chroma.from_documents(
        docs,
        embeddings,
        collection_name=collection_name
    )

    return vector_store

# Crear los stores para cada agente
hr_vector = create_vector_store("data/hr_docs.md","hr_docs")
ti_vector = create_vector_store("data/ti_docs.md","ti_docs")
finance_vector = create_vector_store("data/finance_docs.md","finance_docs")

hr_retriever = hr_vector.as_retriever()
ti_retriever = ti_vector.as_retriever()
finance_retriever = finance_vector.as_retriever()

# Prompt RAG
rag_prompt = ChatPromptTemplate.from_template("""
Eres un asistente experto del departamento de {department_name}.

Responde la pregunta usando SOLO el contexto entregado.

Contexto:
{context}

Pregunta:
{question}
""")

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Respuesta del RAG
def rag_answer(retriever, department_name, question):

    docs = retriever.invoke(question)

    context = "\n".join([d.page_content for d in docs])

    chain = rag_prompt | llm

    response = chain.invoke(
        {
            "department_name": department_name,
            "context": context,
            "question": question
        }
    )

    return str(response.content)
