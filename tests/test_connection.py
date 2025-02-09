from sqlmodel import select

from adapted_work.database.tables import Andalucia


def test_insert_andalucia(db_session):
    """Prueba insertar y consultar datos en la tabla andalucia."""
    url = Andalucia(id=1, url="test")
    db_session.add(url)
    db_session.commit()


def test_get_data(db_session):
    query = select(Andalucia)
    result = db_session.exec(query).first()

    assert result is not None
