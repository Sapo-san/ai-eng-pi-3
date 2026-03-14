from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from tracing.langfuse_config import langfuse_handler

# Prompt
orchestrator_prompt = ChatPromptTemplate.from_template("""
Eres un agente orquestador.

Tu trabajo es decidir que agente especialista debe responder la pregunta del usuario.

Los agentes disponibles son:

ti_agent → preguntas de soporte técnico o ti

hr_agent → preguntas sobre recursos humanos

finance_agent → preguntas finanzas o reportes sobre la empresa

Responde SOLO con el nombre del agente adecuado. En caso no haber un agente adecuado responder "invalid"

Pregunta:
{question}
""")

# Instancia del LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Cadena 
orchestrator_chain = orchestrator_prompt | llm

# Configuracion para tracing
config: RunnableConfig = {
    "callbacks": [langfuse_handler],
    "run_name": "orquestador"
}

# Orquestador
def route_question(question: str):
    '''
    Recibe una pregunta del usuario,
    responde el nombre del agente a que corresponde
    enrutar la pregunta.
    '''

    response = orchestrator_chain.invoke(
        {
            "question": question
        },
        config=config
        )

    agent = response.content.strip()

    if agent not in ['ti_agent','hr_agent','finance_agent','invalid']:
        print('> Respuesta inválida de orquestador detectada')
        return 'invalid'

    return agent


