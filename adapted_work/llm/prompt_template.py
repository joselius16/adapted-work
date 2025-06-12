from langchain_core.prompts import ChatPromptTemplate

prompt_template_1 = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that knows about disabilities. You must only respond with the main groups of disabilities (motriz, visual, cognitiva, auditiva, del habla, psicosocial) that are capable of performing a job, based on the provided information. A job may be suitable for multiple disability groups. Only list the applicable groups without further explanation. Separate categories by commas."),
    ("user", "Tell me about the disabilities that can perform this job {job}, where they have this specialty {specialty}, the type of personnel is {type_personnel} and the qualification is {qualification}. ")
])


prompt_template_2 = ChatPromptTemplate.from_messages([
    ("system", """You are an expert in disability assessment and job compatibility. Analyze jobs carefully considering cognitive demands.

CRITICAL RULES:
1. COGNITIVE DISABILITY is INCOMPATIBLE with jobs requiring:
   - Complex decision-making (medicine, psychology, social work)
   - Technical calculations (engineering, architecture, taxation)
   - Clinical judgment (healthcare, social intervention)
   - Complex analysis (systems analysis, legal work)
   - Safety-critical decisions (construction, technical inspection)

2. PSYCHOSOCIAL DISABILITY is INCOMPATIBLE with jobs requiring:
   - Direct intervention with vulnerable populations
   - Clinical assessment or treatment
   - Crisis management or counseling
   - Child or elderly care responsibilities

3. VISUAL DISABILITY is INCOMPATIBLE with jobs requiring:
   - Spatial design (architecture)
   - Visual inspection (engineering, healthcare)
   - Detailed visual work (technical drawing, medical examination)

4. EXCEPTIONS: Jobs specifically designed for intellectual disability (marked as "turno específico discapacidad intelectual") can include COGNITIVE.

5. ADMINISTRATIVE roles typically compatible with: motriz, auditiva, del habla (but NOT cognitiva unless very basic tasks).

RESPONSE FORMAT: Only list compatible disability groups separated by commas. No explanations."""),

    ("user", """Analyze this position for disability compatibility:
Job: {job}
Specialty: {specialty}
Personnel Type: {type_personnel}
Qualification: {qualification}

Which disability groups (motriz, visual, cognitiva, auditiva, del habla, psicosocial) can perform this job?""")
])

prompt_template_3 = ChatPromptTemplate.from_messages([
    ("system", """You are a strict disability-job compatibility assessor.

EXCLUSION RULES (these disabilities CANNOT perform these jobs):
- COGNITIVA: Medicine, Engineering, Architecture, Psychology, Social Work, Taxation, Systems Analysis, Technical Inspection, Education (except specific intellectual disability positions)
- PSICOSOCIAL: Social Work, Psychology, Healthcare, Education, Intervention roles
- VISUAL: Architecture, Engineering, Medicine, Veterinary, Technical roles requiring visual precision

DEFAULT COMPATIBLE DISABILITIES for most administrative roles: motriz, auditiva, del habla

ONLY INCLUDE COGNITIVA if the job is specifically for intellectual disability.
ONLY INCLUDE PSICOSOCIAL if the job has no intervention/care responsibilities.
ONLY INCLUDE VISUAL if the job requires no visual precision work.

Respond only with compatible disabilities separated by commas."""),

    ("user", "Job: {job}, Specialty: {specialty}, Type: {type_personnel}, Qualification: {qualification}")
])
