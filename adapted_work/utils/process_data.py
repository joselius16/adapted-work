from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import engine
from adapted_work.database.tables import Jobs
from adapted_work.llm.prompt_template import (prompt_template_1,
                                              prompt_template_2,
                                              prompt_template_3)
from adapted_work.settings import settings


def load_llm():
    llm = ChatOllama(
        model=settings.ollama_model,
        temperature=0.0,
        num_predict=256
    )

    chain = prompt_template_2 | llm

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
                    logger.info(f"Url {data.ext_url} already in database.")
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
