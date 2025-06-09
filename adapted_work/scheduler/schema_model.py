from pydantic import Field
from pydantic_settings import BaseSettings


class ComunityBaseUrl(BaseSettings):
    andalucia: str = Field("https://www.juntadeandalucia.es/organismos/iaap/areas/empleo-publico/procesos-selectivos/detalle/", description="Url from where we have to insert numbers")
    aragon: str = Field("https://aplicaciones.aragon.es/oepc/oepc?dga_accion_app=mostrar_convocatoria&convocatoria_codigo=", description="Url from where we have to insert numbers")
    extremadura: str = Field("https://www.juntaex.es/temas/trabajo-y-empleo/empleo-publico/buscador-de-empleo-publico/-/convocatoria/", description="Url from where we have to insert numbers")
    murcia: str = Field("https://empleopublico.carm.es/web/pagina?IDCONTENIDO=62006&IDTIPO=100&RASTRO=c%24m61986%2C61991&BUSCAR_POR=CUERPO_OFERTA&CUERPOS_OFERTABLES=0&ESTADOS_OPOSICIONES=0&Buscar=Buscar", description="Url from Murcia")


class CommunityNames:
    andalucia: str = "Andalucia"
    aragon: str = "Aragon"
    extremadura: str = "Extremadura"
    murcia: str = "Murcia"


class RangeId:
    start_id: str = "start_id"
    end_id: str = "end_id"


# Web pages ids
web_pages_ids = "adapted_work/scheduler/web_pages_id.json"


comunity_names = CommunityNames()
comunity_base_url = ComunityBaseUrl()
range_id = RangeId()
