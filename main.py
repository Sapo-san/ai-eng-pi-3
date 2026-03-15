# Cargar variables de entorno (no borrar)
from dotenv import load_dotenv
load_dotenv()

from agents.orquestador import run_orchestrator

question = "¿ingresos de diciembre del año anterior?"

from tracing.langfuse_config import langfuse_handler


ev = run_orchestrator(question)

print(ev)