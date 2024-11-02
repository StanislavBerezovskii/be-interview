from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from app.core.db import get_db
# Rerouted the imports via app/models/__init__.py file for readability and briefness
from app.models import CreateLocation, Location

# Moved the locations prefix to the router for readability and briefness
router = APIRouter(prefix="/{organisation_id}/locations")


# Changed the endpoint to "/{organisation_id}/locations" for RESTful Consistency
# Implemented the create_location() endpoint
@router.post("/")
def create_location(
        organisation_id: int,
        create_location: CreateLocation,
        session: Session = Depends(get_db)
):
    """Creates a location."""
    location = Location(
        organisation_id=organisation_id,
        location_name=create_location.location_name,
        longitude=create_location.longitude,
        latitude=create_location.latitude
    )
    session.add(location)
    session.commit()
    session.refresh(location)
    return location


# Refactored the get_organisation_locations() endpoint to avoid double DB queries
@router.get("/")
def get_organisation_locations(organisation_id: int, session: Session = Depends(get_db)):
    """Gets all locations for an organisation."""
    db_locations_data = session.exec(
        select(Location.location_name, Location.longitude, Location.latitude)
        .where(Location.organisation_id == organisation_id)
    ).all()

    results = [
        {"location_name": location_name, "location_longitude": longitude, "location_latitude": latitude}
        for location_name, longitude, latitude in db_locations_data
    ]

    return results
