from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    schema_database: str = "public"
    log_path: str = Field("logs/webscraping.log", env="LOG_PATH")
    database_uri: str = Field(..., env="DATABASE_URI")

    # Andalucia
    base_url_andalucia: str = Field(
        "https://www.juntadeandalucia.es/organismos/iaap/areas/empleo-publico/procesos-selectivos/detalle/",
        env="BASE_URL_ANDALUCIA",
    )
    start_id_andalucia: int = Field(514702, env="START_ID_ANDALUCIA")
    end_id_andalucia: int = Field(514714, env="END_ID_ANDALUCIA")

    class Config:
        env_file = ".env"


class tableNames:
    comunity: str = "comunity"
    comunity_type: str = "comunity_type"


class id_comunities:
    andalucia: int = 1
    aragon: int = 2
    extremadura: int = 3
    murcia: int = 4


table_names = tableNames()
settings = Settings()
comunities_codes = id_comunities()
