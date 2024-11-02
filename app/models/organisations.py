from sqlmodel import Field

from app.models import Base


class CreateOrganisation(Base):
    name: str


class Organisation(Base, table=True):
    __tablename__ = "organisation"
    id: int | None = Field(primary_key=True)
    name: str
