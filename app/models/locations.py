from sqlmodel import Field, Relationship

from app.models import Base, Organisation


class Location(Base, table=True):
    __tablename__ = "locations"
    id: int | None = Field(primary_key=True)
    organisation_id: int = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship()
    location_name: str
    longitude: float
    latitude: float


class CreateLocation(Base):
    organisation_id: int
    location_name: str
    longitude: float
    latitude: float
