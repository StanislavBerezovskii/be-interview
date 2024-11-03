from app.crud.base import CRUDBase
from app.models import Organisation


# Creates a CRUDBase instance to be used in the location endpoints
crud_organisation = CRUDBase(Organisation)
