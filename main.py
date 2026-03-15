# Cargar variables de entorno (no borrar)
from dotenv import load_dotenv
load_dotenv()

from agents.orquestador import run_orchestrator

question = '¿Que ocurre si aparece un portal que lleva a otra dimension?'

ev = run_orchestrator(question)
print(ev)