from sqlalchemy.orm import Session
from sqlmodel import select

from app.crud.base import CRUDBase
from app.models import CreateLocation, Location


class CRUDLocation(CRUDBase):
    def create(self, location_in: CreateLocation, organisation_id: int, session: Session) -> Location:
        """Creates a new location instance in the database."""
        location_in_data = location_in.dict()
        db_location = Location(**location_in_data, organisation_id=organisation_id)
        session.add(db_location)
        session.commit()
        session.refresh(db_location)
        return db_location

    def get_organisation_locations(self, organisation_id: int, session: Session) -> list[dict]:
        """Gets all locations for an organisation."""
        db_locations_data = session.execute(
            select(Location.location_name, Location.longitude, Location.latitude)
            .where(Location.organisation_id == organisation_id)
        ).all()

        results = [
            {"location_name": location_name, "location_longitude": longitude, "location_latitude": latitude}
            for location_name, longitude, latitude in db_locations_data
        ]

        return results


crud_location = CRUDLocation(Location)
