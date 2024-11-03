from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.locations import crud_location
from app.crud.organisations import crud_organisation


def check_location_name_duplicate(location_name: str, session: Session) -> None:
    """Checks if a location with the given name already exists in the database."""
    obj_id = crud_location.get_id_by_name(location_name, session)
    if obj_id is not None:
        raise HTTPException(
            status_code=422,
            detail=f"A Location with the name {location_name} already exists"
        )


def check_organisation_name_duplicate(organisation_name: str, session: Session) -> None:
    """Checks if an organisation with the given name already exists in the database."""
    obj_id = crud_organisation.get_id_by_name(organisation_name, session)
    if obj_id is not None:
        raise HTTPException(
            status_code=422,
            detail=f"An Organisation with the name {organisation_name} already exists"
        )
