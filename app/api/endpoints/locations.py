from fastapi import APIRouter, Depends, Query
from sqlmodel import select, Session

from app.api.endpoints.validators import check_location_name_duplicate
from app.core.db import get_db
from app.crud.locations import crud_location
# Rerouted the imports via app/models/__init__.py file for readability and briefness
from app.models import Location
from app.schemas import CreateLocation

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
    check_location_name_duplicate(location_name=location_create.location_name, session=session)
    new_location = crud_location.create(
        location_in=location_create,
        organisation_id=organisation_id,
        session=session
    )
    return new_location


# Refactored the get_organisation_locations() endpoint to avoid double DB queries
# See the locations.py file in the app.crud folder for more details
@router.get("/")
def get_organisation_locations(
        organisation_id: int,
        min_longitude: float = Query(None, alias="bounding_box_min_longitude"),
        max_longitude: float = Query(None, alias="bounding_box_max_longitude"),
        min_latitude: float = Query(None, alias="bounding_box_min_latitude"),
        max_latitude: float = Query(None, alias="bounding_box_max_latitude"),
        session: Session = Depends(get_db)):
    """Endpoint to get all location instances for an organisation.
    Accepts a coordinate bounding box in the form of min_longitude, max_longitude, min_latitude, max_latitude"""
    bounding_box = (
        (min_longitude, max_longitude, min_latitude, max_latitude)
        if min_longitude is not None
        and max_longitude is not None
        and min_latitude is not None
        and max_latitude is not None else None
    )

    locations = crud_location.get_organisation_locations(
        organisation_id=organisation_id,
        session=session,
        bounding_box=bounding_box
    )
    return locations
