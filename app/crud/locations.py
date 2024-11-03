from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlmodel import select

from app.crud.base import CRUDBase
from app.models import Location
from app.schemas import CreateLocation


class CRUDLocation(CRUDBase):
    def create(self, location_in: CreateLocation, organisation_id: int, session: Session) -> Location:
        """Creates a new location instance in the database.
        Redefined to include the organisation_id which is not in the CreateLocation schema"""
        location_in_data = location_in.dict()
        db_location = Location(**location_in_data, organisation_id=organisation_id)
        session.add(db_location)
        session.commit()
        session.refresh(db_location)
        return db_location

    def get_organisation_locations(
            self,
            organisation_id: int,
            session: Session,
            bounding_box: tuple[float, float, float, float] = None) -> list[dict]:
        """Gets all locations for an organisation.
        Refactored the inefficient initial task query to avoid double DB calls"""
        query = select(Location.location_name, Location.longitude, Location.latitude).where(
            Location.organisation_id == organisation_id
        )

        # Apply bounding box filtering if the bounding box is provided
        if bounding_box:
            min_longitude, max_longitude, min_latitude, max_latitude = bounding_box
            query = query.where(
                and_(
                    Location.longitude >= min_longitude,
                    Location.longitude <= max_longitude,
                    Location.latitude >= min_latitude,
                    Location.latitude <= max_latitude
                )
            )

        db_locations_data = session.execute(query).all()
        return [{"location_name": loc[0], "longitude": loc[1], "latitude": loc[2]} for loc in db_locations_data]



        """db_locations_data = session.execute(
            select(Location.location_name, Location.longitude, Location.latitude)
            .where(Location.organisation_id == organisation_id)
        ).all()

        results = [
            {"location_name": location_name, "location_longitude": longitude, "location_latitude": latitude}
            for location_name, longitude, latitude in db_locations_data
        ]

        return results"""

    def get_id_by_name(self, location_name: str, session: Session) -> int:
        """Returns the ID of a location by name from the database.
        Redefined to correctly handle the location_name field if the Location model"""
        db_location_id = session.execute(
            select(Location.id).where(Location.location_name == location_name)
        )
        return db_location_id.scalars().first()


# Creates a CRUDLocation instance to be used in the location endpoints
crud_location = CRUDLocation(Location)
