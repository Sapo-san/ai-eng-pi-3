from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Evaluation(BaseModel):
    score: int = Field(
        description="Puntaje de la respuesta entre 1 y 10"
    )
    feedback: str = Field(
        description="Explicación breve de máximo 25 palabras"
    )

# Prompt template del evaluador
with open("prompts/evaluador.txt", mode='r') as prompt_file:
    prompt_evaluador = prompt_file.read()

evaluator_prompt = ChatPromptTemplate.from_template(prompt_evaluador)

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).with_structured_output(Evaluation)

# Cadena del evaluador
evaluator_chain = evaluator_prompt | llm