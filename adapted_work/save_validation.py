from adapted_work.router.comunities.andalucia.save_andalucia.extract import \
    save_andalucia
from adapted_work.router.comunities.aragon.save_aragon.extract import \
    save_aragon
from adapted_work.router.comunities.extremadura.save_extremadura.extract import \
    save_extremadura
from adapted_work.router.comunities.murcia.save_murcia.extract import \
    save_murcia
from adapted_work.settings import settings

url_api_murcia = "https://empleopublico.carm.es/web/pagina?IDCONTENIDO=62006&IDTIPO=100&RASTRO=c%24m61986%2C61991&BUSCAR_POR=CUERPO_OFERTA&CUERPOS_OFERTABLES=0&ESTADOS_OPOSICIONES=0&Buscar=Buscar"




if __name__ == "__main__":
    save_andalucia("https://www.juntadeandalucia.es/organismos/iaap/areas/empleo-publico/procesos-selectivos/detalle/", settings.start_id_andalucia, settings.end_id_andalucia)
    save_aragon("https://aplicaciones.aragon.es/oepc/oepc?dga_accion_app=mostrar_convocatoria&convocatoria_codigo=", 240118, 240219)
    save_extremadura("https://www.juntaex.es/temas/trabajo-y-empleo/empleo-publico/buscador-de-empleo-publico/-/convocatoria/", 1625, 1626)
    save_murcia(url_api_murcia)
