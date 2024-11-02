from fastapi import APIRouter

# Rerouted the imports via app/api/endpoints/__init__.py file for readability and briefness
from app.api.endpoints import locations_router, organisations_router

api_router = APIRouter()


# Locations_router prefix is left the same for multi-level prefix building
api_router.include_router(locations_router, prefix="/organisations", tags=["locations"])
api_router.include_router(organisations_router, prefix="/organisations", tags=["organisations"])
