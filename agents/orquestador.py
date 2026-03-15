from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableConfig

from langchain.agents import create_agent

from agents.especialistas import hr_agent_tool, ti_agent_tool, finance_agent_tool
from agents.evaluador import evaluator_chain

from tracing.langfuse_config import langfuse_handler


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


tools = [
    hr_agent_tool,
    ti_agent_tool,
    finance_agent_tool
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
Eres un agente orquestador.

Tu trabajo es decidir qué agente especialista debe responder la pregunta.

Los agentes disponibles son:

hr_agent → preguntas sobre recursos humanos  
ti_agent → preguntas sobre soporte técnico o TI  
finance_agent → preguntas sobre finanzas o reportes de la empresa
"""
)

extract_specialist_answer = RunnableLambda(
    lambda result: {
        "question": result["messages"][0].content,
        "answer": result["messages"][-1].content
    }
)

multiagent_chain = agent | extract_specialist_answer | evaluator_chain

def run_orchestrator(question: str):

    config: RunnableConfig = {
        "callbacks": [langfuse_handler],
        "run_name": "multiagent_pipeline",
        "metadata": {
            "langfuse_trace_name": "flujo_multiagente"
        }
    }

    result = multiagent_chain.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config=config
    )

    return result.content