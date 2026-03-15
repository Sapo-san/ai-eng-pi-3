# Cargar variables de entorno (no borrar)
from dotenv import load_dotenv
load_dotenv()

from agents.orquestador import run_orchestrator

question = "¿Cuales son los ingresos del ultimo trimestre?"

from tracing.langfuse_config import langfuse_handler


ev = run_orchestrator(question)

print(ev)