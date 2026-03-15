from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from langchain.agents import create_agent

from agents.especialistas import hr_agent_tool, ti_agent_tool, finance_agent_tool
from agents.evaluador import evaluator_chain

from tracing.langfuse_config import langfuse_handler

from langfuse import propagate_attributes

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Tools
tools = [
    hr_agent_tool,
    ti_agent_tool,
    finance_agent_tool
]

# Prompt
with open("prompts/orquestador.txt", mode='r') as prompt_file:
    prompt_orquestador = prompt_file.read()

# Agente
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt_orquestador
)

# ------------------------------------------------------------
def debug_orchestrator(result):
    '''
    Imprime la respuesta del orquestador en pantalla
    '''
    for elem in result['messages']:
        if isinstance(elem, HumanMessage):
            continue
        elif isinstance(elem, AIMessage):
            if len(elem.tool_calls) > 0:
                for tc in elem.tool_calls:
                    print (f'Orquestador | Tool call: {tc['name']}')
                continue
            if elem.content != '':
                print(f"Orquestador | Respuesta: {elem.content}")
        
        elif isinstance(elem, ToolMessage):
            print (f'Especialista {elem.name} : {elem.content}')
    return result

debug_node = RunnableLambda(debug_orchestrator)
# ------------------------------------------------------------

# Extractor de respuesta (Se usa para pasar a la sgte cadena)
extract_specialist_answer = RunnableLambda(
    lambda result: {
        "question": result["messages"][0].content, # type: ignore
        "answer": result["messages"][-1].content # type: ignore
    }
)

# ------------------------------------------------------------

# Cadena
multiagent_chain = agent | debug_orchestrator | extract_specialist_answer | evaluator_chain

# ------------------------------------------------------------

def run_orchestrator(question: str):
    '''
    Ejecuta el flujo multiagente
    '''

    with propagate_attributes(trace_name="Flujo Multiagente Aperture"):# Setear nombre del flujo

        config: RunnableConfig = {
            "callbacks": [langfuse_handler],
            "run_name": "multiagent_pipeline"
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

        print(f'Evaluador | score: {result.score}') # type: ignore
        print(f'Evaluador | score: {result.feedback}') # type: ignore

        return result