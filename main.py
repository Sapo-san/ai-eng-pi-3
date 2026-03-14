# Cargar variables de entorno (no borrar)
from dotenv import load_dotenv
load_dotenv()

from agents.orquestador import route_question
from agents.especialistas import hr_agent, ti_agent, finance_agent
from agents.evaluador import evaluate_answer

question = "¿Cuántos días de vacaciones tienen los empleados?"

agent = route_question(question)

if agent == "hr_agent":
    answer = hr_agent(question)

elif agent == "ti_agent":
    answer = ti_agent(question)

elif agent == "finance_agent":
    answer = finance_agent(question)

else:
    answer = "No pude clasificar la pregunta."

evaluation = evaluate_answer(question, str(answer))

print("Respuesta:")
print(answer)

print("\nEvaluación:")
print(evaluation)
