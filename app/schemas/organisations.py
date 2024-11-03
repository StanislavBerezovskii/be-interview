from pydantic import BaseModel, Extra, Field
from typing import Optional


class CreateOrganisation(BaseModel):
    """Pydantic schema for creating a new Organisation instance in the database"""
    name: str = Field(..., min_length=1, max_length=100, examples=["Example Organisation"])

    class Config:
        extra = Extra.forbid
