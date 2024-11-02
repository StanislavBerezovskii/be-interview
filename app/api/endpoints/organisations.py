from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, Session

from app.core.db import get_db
# Rerouted the imports via app/models/__init__.py file for readability and briefness
from app.models import CreateOrganisation, Organisation

router = APIRouter()


# TODO: Changed the endpoint to "/" for RESTful Consistency
@router.post("/", response_model=Organisation)
def create_organisation(
        create_organisation: CreateOrganisation,
        session: Session = Depends(get_db)
) -> Organisation:
    """Creates an organisation."""
    organisation = Organisation(name=create_organisation.name)
    session.add(organisation)
    session.commit()
    session.refresh(organisation)
    return organisation


@router.get("/", response_model=list[Organisation])
def get_organisations(
        session: Session = Depends(get_db)
) -> list[Organisation]:
    """Gets all organisations."""
    organisations = session.exec(select(Organisation)).all()
    return organisations


@router.get("/{organisation_id}", response_model=Organisation)
def get_organisation(
        organisation_id: int,
        session: Session = Depends(get_db)
) -> Organisation:
    """Gets an organisation by id."""
    organisation = session.get(Organisation, organisation_id)
    if organisation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    return organisation


# TODO: Moved the locations endpoints to their own file locations.py for RESTful consistency
