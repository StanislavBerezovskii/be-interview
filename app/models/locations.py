from sqlmodel import Field, Relationship

from app.models import Base, Organisation


class Location(Base, table=True):
    """Database Location model"""
    __tablename__ = "location"
    id: int | None = Field(primary_key=True)
    organisation_id: int = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship()
    location_name: str
    longitude: float
    latitude: float

