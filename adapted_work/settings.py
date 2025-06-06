from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    log_path: str = Field("logs/webscraping.log", env="LOG_PATH")
    database_uri: str = Field(..., env="DATABASE_URI")

    # Ollama model
    ollama_model: str = Field(..., env="OLLAMA_MODEL")
    start_id_andalucia: int = Field(514009, env="START_ID_ANDALUCIA")
    end_id_andalucia: int = Field(514116, env="END_ID_ANDALUCIA")

    class Config:
        env_file = ".env"


class DatabaseSettings:
    class TableName:
        community = "community"
        jobs = "jobs"

    class schema:
        schema_database = "empleo"

    class community_id:
        andalucia = 1
        aragon = 2
        extremadura = 3
        murcia = 4

class ComunityBaseUrl:
    base_url_andalucia: str = Field("https://www.juntadeandalucia.es/organismos/iaap/areas/empleo-publico/procesos-selectivos/detalle/")


class CommunityNames:
    andalucia: str = "Andalucia"
    aragon: str = "Aragon"
    extremadura: str = "Extremadura"
    murcia: str = "Murcia"

settings = Settings()
database_settings = DatabaseSettings()
