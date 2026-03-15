# Proyecto Integrador M3 | Henry AI Engineering

El entorno de desarrollo donde se creó y desarrolló este repositorio es WSL (Ubuntu) dentro de Windows 11 con `uv` y Python 3.12 instalado.

**Configurar variables de entorno:**

```bash
cp .env.example .env
```

Nota: Completar variables `OPENAI_API_KEY`, `LANGFUSE_SECRET_KEY` y `LANGFUSE_PUBLIC_KEY` en `.env` par ejecutar.

---

**Para instalar dependencias** detalladas en uv.lock

```bash
# Instalar dependencias
uv sync

# Activar entorno virtual
source .venv/bin/activate
```

## Ejecución

La ejecución del PI es celda a celda a través del notebook `main.ipynb`.

## Consideraciones y otros

Para el desarrollo de este PI seguí lo indicado en `instrucciones.md` que es un copiar-pegar de lo ubicado en la lecture [M3PI | Proyecto](https://www.app.soyhenry.com/my-cohort/c1be21ab-e806-4e47-9052-446e5dcff8f8/lecture/bfeccb2b-2d9c-4188-b0ae-26f4bc58e1a7)

El bonus del agente evaluador con la Score API de LangFuse está implementado.

Dado que la tarea solicitaba utilizar LangChain, eso fue lo que utilicé pero creo que habría sido mas sencillo utilizar LangGraph para la implementación de la arquitectura para evitar el problema que describo a continuación:

Al usar LangChain, tuve que implementar un agente con tools para que el redireccionamiento a los agentes especialistas funcionara correctamente y poder así tracear el flujo con LangFuse de manera sencilla. El problema de esto es que el agente orquestador luego de consultar la tool (es decir, el agente especialista) hace una llamada adicional a la API para responder él cuando la idea es que el especialista responda directamente. 

La solucion parche que implementé para lo anterior es que le especifico al agente en el prompt que no debe parafrasear y que debe devolver como respuesta el resultado exacto de la tool.

Con LangGraph esto se habría evitado ya que el agente especializado seria el ultimo nodo del flujo o le pasaría directamente la respuesta al agente evaluador, evitando esa API call adicional.

El tracing está implementado con Langfuse como se solicitó, utilizando callbacks. El callback se encarga de mantener el mismo Trace ID y Trace Name dentro del flujo y se puede observar en el Dashboard de LangFuse.

Respecto al nodo `debug_orchestrator` que aparece en las cadenas en `agents/orquestador.py`, su unica función es imprimir los resultados en pantalla para que el notebook `main.ipynb` tenga visibilidad de las respuestas ademas de las evaluaciones. Todo lo demás puede observarse por el dashboard de Langfuse.
