from sqlmodel import Field

from app.models import Base


class Organisation(Base, table=True):
    """Database Organisation model"""
    __tablename__ = "organisation"
    id: int | None = Field(primary_key=True)
    name: str
