from pydantic import BaseModel


class ComunitiesModel(BaseModel):
    """Communities model."""

    id: int
    name: str
