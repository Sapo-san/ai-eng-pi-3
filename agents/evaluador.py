from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# Prompt template del evaluador
with open("prompts/evaluador.txt", mode='r') as prompt_file:
    prompt_evaluador = prompt_file.read()

evaluator_prompt = ChatPromptTemplate.from_template(prompt_evaluador)

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Cadena del evaluador
evaluator_chain = evaluator_prompt | llm