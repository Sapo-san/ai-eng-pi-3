from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from tracing.langfuse_config import langfuse_handler, langfuse



# Prompt
evaluation_prompt = ChatPromptTemplate.from_template("""
Eres un evaluador de respuestas dentro de una empresa.

Debes evaluar la calidad de la respuesta entregada por un agente especialista.

Pregunta del usuario:
{question}

Respuesta del agente:
{answer}

Evalúa la respuesta considerando:

- precisión
- claridad
- utilidad

Entrega:

score: número entre 1 y 10  
feedback: breve explicación de 25 palabras o menos.

Responde SOLO en este formato:

score: X
feedback: texto
""")

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Cadena
evaluation_chain = evaluation_prompt | llm

def evaluate_answer(question: str, answer: str):

    # Config para traceo
    config: RunnableConfig = {
        "callbacks": [langfuse_handler],
        "run_name": "agente_evaluador"
    }


    response = evaluation_chain.invoke({
        "question": question,
        "answer": answer
    },
    config=config
    )

    print(f">> {response.content}")

    return response.content
