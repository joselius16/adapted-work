from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import engine
from adapted_work.database.tables import Jobs

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


def load_llm():
    llm = ChatOllama(
        model="gemma3:4b",
        temperature=0.0,
        num_predict=256
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that knows about disabilities. You must only respond with the main groups of disabilities (motriz, visual, cognitiva, auditiva, del habla, psicosocial) that are capable of performing a job, based on the provided information. A job may be suitable for multiple disability groups. Only list the applicable groups without further explanation."),
        ("user", "Tell me about the disabilities that can perform this job {job}, where they have this specialty {specialty}, the type of personnel is {type_personnel} and the qualification is {qualification}. ")
    ])

    chain = prompt_template | llm

    return chain


def llm_prediction(chain, data):
    response = chain.invoke({
        "job": data.title,
        "specialty": data.specialty,
        "type_personnel": data.type_personnel,
        "qualification": data.qualification
    })

    return response.content


def save_into_database(data_administration):
    try:
        logger.info("Saving into database.")
        with Session(engine) as session:
            # Loading llm
            chain = load_llm()
            for data in data_administration:
                statement = select(Jobs).where(Jobs.ext_url == data.ext_url)
                result = session.exec(statement).first()

                if result:
                    logger.info(f"Url {data.url} already in database.")
                    continue
                
                # Predict with llm
                data.pred_disability = llm_prediction(chain, data)
                # Adding into database
                session.add(data)
                logger.info(f"saving: {data.ext_url}")
            session.commit()

        logger.info("Executed succesfully.")

    except Exception as e:
        logger.error(f"Cannot save into database: {e}")
