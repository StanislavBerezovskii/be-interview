from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, Session

from app.api.endpoints.validators import check_organisation_name_duplicate
from app.core.db import get_db
from app.crud.organisations import crud_organisation
# Rerouted the imports via app/models/__init__.py file for readability and briefness
from app.models import Organisation
from app.schemas import CreateOrganisation

router = APIRouter()


# Changed the endpoint to "/" for RESTful Consistency
@router.post("/", response_model=Organisation)
def create_organisation(
        organisation_create: CreateOrganisation,
        session: Session = Depends(get_db)
) -> Organisation:
    """Creates an organisation."""
    check_organisation_name_duplicate(organisation_name=organisation_create.name, session=session)
    new_organisation = crud_organisation.create(obj_in=organisation_create, session=session)
    return new_organisation


@router.get("/", response_model=list[Organisation])
def get_organisations(
        session: Session = Depends(get_db)
) -> list[Organisation]:
    """Endpoint that returns all organisation instances from the database."""
    organisations = crud_organisation.get_all(session=session)
    return organisations


@router.get("/{organisation_id}", response_model=Organisation)
def get_organisation(
        organisation_id: int,
        session: Session = Depends(get_db)
) -> Organisation:
    """Endpoint that returns an organisation instance from the database."""
    organisation = crud_organisation.get(obj_id=organisation_id, session=session)
    return organisation


# Moved the locations endpoints to their own file locations.py for RESTful consistency
