from rag.vector_store import hr_retriever, ti_retriever, finance_retriever
from rag.vector_store import rag_answer

from langchain.tools import tool


@tool("hr_agent")
def hr_agent_tool(question: str) -> str:
    """Responder preguntas sobre recursos humanos."""
    return rag_answer(hr_retriever, "Recursos Humanos", question)


@tool("ti_agent")
def ti_agent_tool(question: str) -> str:
    """Responder preguntas sobre soporte técnico."""
    return rag_answer(ti_retriever, "Soporte TI", question)

@tool("finance_agent")
def finance_agent_tool(question: str) -> str:
    """Responder preguntas sobre finanzas de la empresa."""
    return rag_answer(finance_retriever, "Finanzas", question)