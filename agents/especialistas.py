from rag.vector_store import hr_retriever, ti_retriever, finance_retriever
from rag.vector_store import rag_answer


def hr_agent(question):
    return rag_answer('agente_hr', hr_retriever, 'Recursos Humanos', question)

def ti_agent(question):
    return rag_answer('agente_ti', ti_retriever, 'Soporte Ti', question)

def finance_agent(question):
    return rag_answer('agente_finanzas', finance_retriever, 'Finanzas', question)