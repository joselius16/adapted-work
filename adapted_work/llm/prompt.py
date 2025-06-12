from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from adapted_work.llm.prompt_template import (prompt_template_1,
                                              prompt_template_2,
                                              prompt_template_3)
from adapted_work.settings import settings

llm = ChatOllama(
    model=settings.ollama_model,
    temperature=0.2,
    num_predict=256
)

chain = prompt_template_1 | llm

response = chain.invoke({
    "job": "AGX00C22-Convocatoria al Cuerpo Superior de Administradores",
    "specialty": "AGX00-Superior Administradores, A1",
    "type_personnel": "AGX00-Superior Administradores, A1",
    "qualification": "Doctorado, Licenciatura, Ingeniería, Arquitectura o Grado"
})

print(response.content)
