from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="gemma3:4b",
    temperature=0.2,
    num_predict=256
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that knows about disabilities. You must only respond with the main groups of disabilities (motriz, visual, cognitiva, auditiva, del habla, psicosocial) that are capable of performing a job, based on the provided information. A job may be suitable for multiple disability groups. Only list the applicable groups without further explanation."),
    ("user", "Tell me about the disabilities that can perform this job {job}, where they have this specialty {specialty}, the type of personnel is {type_personnel} and the qualification is {qualification}. ")
])

chain = prompt_template | llm

response = chain.invoke({
    "job": "AGX00C22-Convocatoria al Cuerpo Superior de Administradores",
    "specialty": "AGX00-Superior Administradores, A1",
    "type_personnel": "AGX00-Superior Administradores, A1",
    "qualification": "Doctorado, Licenciatura, Ingeniería, Arquitectura o Grado"
})

print(response.content)