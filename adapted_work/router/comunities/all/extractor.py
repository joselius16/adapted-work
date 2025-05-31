from sqlmodel import select

from adapted_work.database.tables import Community
from adapted_work.router.comunities.all.schema_model import ComunitiesModel


def get_comunities(db):
    """Get communities."""
    query = select(Community.id.label("id"), Community.name.label("name"))
    result = db.exec(query).all()
    return result


def parse_comunities(result_comunities):
    """Parse communities."""
    comunities = []
    for com in result_comunities:
        comunities.append(ComunitiesModel(id=com.id, name=com.name))

    return comunities
