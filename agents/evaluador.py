from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# Prompt del evaluador
evaluator_prompt = ChatPromptTemplate.from_template("""
res un evaluador de respuestas dentro de una empresa.

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


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

evaluator_chain = evaluator_prompt | llm