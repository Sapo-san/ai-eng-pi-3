from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from rag.vector_store import hr_retriever, ti_retriever, finance_retriever

# Prompt RAG
with open("prompts/especialista.txt", mode='r') as prompt_file:
    prompt_especialista = prompt_file.read()

rag_prompt = ChatPromptTemplate.from_template(prompt_especialista)

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Especialista RAG
def rag_answer(retriever, department_name, question):
    '''
    Plantilla de agente especialista.
    '''

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


# ------------------------------------------------
# Definicion de agentes especialistas (como tools)
# ------------------------------------------------

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