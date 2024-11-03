from pydantic import BaseModel, Extra, Field


class CreateLocation(BaseModel):
    """Pydantic schema for creating a new Location instance in the database"""
    location_name: str = Field(..., min_length=1, max_length=100, examples=["Example Location"])
    longitude: float = Field(..., ge=-180, le=180, examples=[0.0])
    latitude: float = Field(..., ge=-90, le=90, examples=[0.0])

    class Config:
        extra = Extra.forbid
