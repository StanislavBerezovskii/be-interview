from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from app.core.db import get_db
from app.crud.locations import crud_location
# Rerouted the imports via app/models/__init__.py file for readability and briefness
from app.models import CreateLocation, Location

# Moved the locations prefix to the router for readability and briefness
router = APIRouter(prefix="/{organisation_id}/locations")


# Changed the endpoint to "/{organisation_id}/locations" for RESTful Consistency
# Implemented the create_location() endpoint
@router.post("/", response_model=Location)
def create_location(
        organisation_id: int,
        location_create: CreateLocation,
        session: Session = Depends(get_db)
):
    """Endpoint to create location instances."""
    new_location = crud_location.create(
        location_in=location_create,
        organisation_id=organisation_id,
        session=session
    )
    return new_location


# Refactored the get_organisation_locations() endpoint to avoid double DB queries
@router.get("/")
def get_organisation_locations(organisation_id: int, session: Session = Depends(get_db)):
    """Endpoint to get all location instances for an organisation."""
    locations = crud_location.get_organisation_locations(organisation_id=organisation_id, session=session)
    return locations
